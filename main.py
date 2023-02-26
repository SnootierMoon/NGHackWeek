from bs4 import BeautifulSoup
from tqdm.asyncio import tqdm_asyncio
import aiohttp, asyncio
import functools
import re
import sqlite3

base_url = "https://satsearch.co"

class Product:
    def __init__(self, name, url, specs):
        self.name = name
        self.url = url
        self.specs = specs

    def fix_spec_name(name):
        return re.sub("[^a-zA-Z_0-9]+", "_", name).strip("_").lower()

# get product urls from the data of a search page async def search_page_product_urls(soup):
async def search_page_product_urls(soup):
    search_results = soup.find_all("div", {"class": "search-results"})[0]
    return [ (item.get_text(), base_url + item["href"])
            for item in search_results.find_all("a", href=True)
            if "/products/" in item["href"] ]

# search the nth page for product urls
async def search_nth_page_product_urls(session, product_name, page_num):
    search_url = f"{base_url}/products/search/{product_name}?page={page_num}"

    async with session.get(search_url) as response:
        soup = BeautifulSoup(await response.text(), "html.parser")
        return await search_page_product_urls(soup)

# given a product name, asynchronously search on all search pages for the
# product online and get urls for all products associated with that name
async def search_product_urls(session, product_name):
    search_url = f"{base_url}/products/search/{product_name}?page=1"

    print("Getting main search page")

    async with session.get(search_url) as response:
        soup = BeautifulSoup(await response.text(), "html.parser")

        last_page_href = next(filter(
            lambda item: "Last" in item,
            soup.find_all("a", {"class": "page-link"})
            ))["href"]

        page_count = int(re.findall("\d+", last_page_href)[-1])
        product_count = int(re.search("\d+", soup.find(
            string=lambda text: "products found" in str(text).lower()
            ).parent.get_text()).group(0))

        print(f"Found {page_count} pages, with {product_count} results")

        product_search_tasks = []
        for page_num in range(2, page_count + 1):
            fut = search_nth_page_product_urls(session, product_name, page_num)
            product_search_tasks.append(asyncio.ensure_future(fut))

        product_urls = await search_page_product_urls(soup)

        print()
        print("Retrieving product urls")
        for page_product_urls in await tqdm_asyncio.gather(*product_search_tasks):
            product_urls.extend(page_product_urls)

        print("Retrieved {count} product urls".format(count=len(product_urls)))

        return product_urls

# get a single product's data from its url
async def get_product(session, name, url):
    async with session.get(url) as response:
        soup = BeautifulSoup(await response.text(), "html.parser")
        specs_table = soup.find("div", {"class": "specs-table"})

        specs = {}
        if specs_table:
            elements = specs_table.find_all("div", {"class": "border-bottom"})
            for i in range(0, len(elements), 2):
                key = Product.fix_spec_name(elements[i].get_text())
                value = elements[i + 1].get_text()
                specs[key] = value

        return Product(name, url, specs)

# given a product name, asynchronously get specs for all products associated
# with that name
async def get_products(session, product_name):
    product_urls = await search_product_urls(session, product_name)

    product_spec_tasks = []

    for name, url in product_urls:
        fut = get_product(session, name, url)
        product_spec_tasks.append(asyncio.ensure_future(fut))

    products = []

    print()
    print("Retrieving product specs")
    for product in await tqdm_asyncio.gather(*product_spec_tasks):
        products.append(product)

    return products

def get_spec_names(products):
    return functools.reduce(
            lambda a,b: a.union(b), 
            [set(prod.specs.keys()) for prod in products])

table_name = "product_specs"
def interactive(product_list):
    spec_names = list(get_spec_names(product_list))
    db = sqlite3.connect(":memory:")


    create_stmt = "CREATE TABLE {}({});".format(
        table_name,
        ",".join(["Name"] + spec_names)
    )
    db.execute(create_stmt)

    for product in product_list:
        keys = ["Name"] + list(product.specs.keys())
        vals = [product.name] + list(product.specs.values())
        insert_stmt = "INSERT INTO {} ({}) VALUES({});".format(
                table_name,
                ",".join(keys),
                ",".join(["?" for x in vals])
        )
        db.execute(insert_stmt, vals)

    print()
    print("Retrieved specs: ")
    for x in spec_names:
        print(" - " + x)

    print()
    print("Use SQL commands in the table:", table_name);
    while True:
        print()
        try:
            stmt = input("SQLite: ")
        except (KeyboardInterrupt, EOFError):
            print()
            break
        try:
            for x in db.execute(stmt).fetchall():
                print("  " + str(x))
        except sqlite3.OperationalError as err:
            print("SQL error:", err)

async def run(product_name):
    async with aiohttp.ClientSession() as session:
        products = await get_products(session, product_name)
        interactive(products)

if __name__ == "__main__":
    product_name = input("Product Name: ")
    asyncio.run(run(product_name))
