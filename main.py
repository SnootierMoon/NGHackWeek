from bs4 import BeautifulSoup, NavigableString
from tqdm.asyncio import tqdm_asyncio as tqdm
import aiohttp, asyncio, functools, re, sqlite3

BASE_URL = "https://satsearch.co"
TABLE_NAME = "product_specs"

class Product:
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.specs = {}

    def add_spec(self, key, val):
        self.specs[key] = val

    def fix_spec_name(spec):
        raw_name = ''.join([x for x in spec if isinstance(x, NavigableString)])
        return re.sub("[^a-zA-Z_0-9]+", "_", raw_name).strip("_").lower()

async def search_page_product_urls(soup):
    search_results = soup.find_all("div", {"class": "search-results"})[0]

    return [ (item.get_text(), BASE_URL + item["href"])
            for item in search_results.find_all("a", href=True)
            if "/products/" in item["href"] ]

async def search_nth_page_product_urls(session, product_name, page_num):
    search_url = f"{BASE_URL}/products/search/{product_name}?page={page_num}"

    async with session.get(search_url) as response:
        soup = BeautifulSoup(await response.text(), "html.parser")
        return await search_page_product_urls(soup)

async def search_product_urls(session, product_name):
    search_url = f"{BASE_URL}/products/search/{product_name}?page=1"

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

        product_search_tasks = [asyncio.ensure_future(search_page_product_urls(soup))]
        for page_num in range(2, page_count + 1):
            fut = search_nth_page_product_urls(session, product_name, page_num)
            product_search_tasks.append(asyncio.ensure_future(fut))

        print()
        print("Retrieving product urls")
        product_urls = [url for urls in await tqdm.gather(*product_search_tasks) 
                        for url in urls]

        print("Retrieved {count} product urls".format(count=len(product_urls)))

        return product_urls

async def get_product(session, product):
    async with session.get(product.url) as response:
        soup = BeautifulSoup(await response.text(), "html.parser")
        specs_table = soup.find("div", {"class": "specs-table"})

        specs = {}
        if specs_table:
            elements = specs_table.find_all("div", {"class": "border-bottom"})
            for i in range(0, len(elements), 2):
                key = Product.fix_spec_name(elements[i])
                if key == "lifetime1": print(url)
                value = elements[i + 1].get_text()
                product.add_spec(key, value)
        return product

# given a product name, asynchronously get specs for all products associated
# with that name
async def get_products(session, product_name):
    product_urls = await search_product_urls(session, product_name)

    product_spec_tasks = []

    for name, url in product_urls:
        product = Product(name, url)
        fut = get_product(session, product)
        product_spec_tasks.append(asyncio.ensure_future(fut))

    print()
    print("Retrieving product specs")
    products = list(await tqdm.gather(*product_spec_tasks))

    return products

def get_spec_names(products):
    return functools.reduce(
            lambda a,b: a.union(b), 
            [set(prod.specs.keys()) for prod in products])

def create_table(db, products, spec_names):
    create_stmt = "CREATE TABLE {}({});".format(
        TABLE_NAME,
        ",".join(["Name"] + spec_names)
    )
    db.execute(create_stmt)

    for product in products:
        keys = ["Name"] + list(product.specs.keys())
        vals = [product.name] + list(product.specs.values())
        insert_stmt = "INSERT INTO {} ({}) VALUES({});".format(
                TABLE_NAME,
                ",".join(keys),
                ",".join(["?" for x in vals])
        )
        db.execute(insert_stmt, vals)

def interactive(products):
    spec_names = list(get_spec_names(products))

    print()
    print("Retrieved specs: ")
    for x in spec_names:
        print(" - " + x)

    db = sqlite3.connect(":memory:")
    create_table(db, products, spec_names)

    print()
    print("Use SQL commands in the table:", TABLE_NAME);
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
