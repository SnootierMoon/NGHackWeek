from bs4 import BeautifulSoup, NavigableString
from tqdm.asyncio import tqdm_asyncio
import aiohttp, asyncio, functools, re, sqlite3

BASE_URL = "https://satsearch.co"
TABLE_NAME = "product_specs"

FLOAT_REGEXP = r"[-+]?[0-9]+(\.[0-9])?([eE][-+]?[0-9]+)?"

gather = asyncio.gather

# stores information about a product
class Product:
    def __init__(self, name, url, specs = {}):
        self.name = name
        self.url = url
        self.specs = {}
        self.int_specs = {}
        for key, val in specs.items():
            self.add_spec(key, val)

    # add two fields
    def add_spec(self, key, val):
        fix_key = Product.fix_spec_name(key)
        self.specs[fix_key] = val
        match = re.search(FLOAT_REGEXP, val)
        if match:
            self.int_specs["Num_" + fix_key] = float(match.group(0))

    def all_specs(self):
        return dict(self.specs, **self.int_specs)

    # make the name work as a SQL field
    def fix_spec_name(spec):
        if isinstance(spec, str):
            raw_name = spec
        # get the string parts of the element to filter out unwanted formats,
        # such as superscripts
        else:
            raw_name = "".join([x for x in spec if isinstance(x, NavigableString)])
        # remove non-alphanumeric characters, replace with underscores
        return re.sub(r"[^a-zA-Z_0-9]+", "_", raw_name).strip("_").lower()

# search through a search page for product urls
async def search_page_product_urls(soup):
    # get search results on search page
    search_results = soup.find("div", {"class": "search-results"})

    # filter url links
    return [ (item.get_text(), BASE_URL + item["href"])
            for item in search_results.find_all("a", href=True)
            if "/products/" in item["href"] ]

# fetch the product urls from the nth search page
async def search_nth_page_product_urls(session, product_name, page_num):
    search_url = f"{BASE_URL}/products/search/{product_name}?page={page_num}"

    # get the search page
    async with session.get(search_url) as response:
        # get the product urls from the page
        soup = BeautifulSoup(await response.text(), "html.parser")
        return await search_page_product_urls(soup)

async def search_product_urls(session, product_name):
    search_url = f"{BASE_URL}/products/search/{product_name}?page=1"

    print("Getting main search page")

    # get the page 1 search page
    async with session.get(search_url) as response:
        soup = BeautifulSoup(await response.text(), "html.parser")

        page_links = soup.find_all("a", {"class": "page-link"})
        if page_links:
            # find the last page number
            last_page_href = next(filter(lambda item: "Last" in item, page_links))["href"]
            page_count = int(re.findall(r"\d+", last_page_href)[-1])
        else:
            # if page-links doesn't exist, there is no pagination because there
            # is only one page
            page_count = 1

        # get total number of products from the page
        product_count_tag = soup.find(string=lambda text: "products found" in str(text).lower()).parent
        product_count = int(re.search(r"\d+", product_count_tag.get_text()).group(0))

        print(f"Found {page_count} pages, with {product_count} results")

        # create a list of futures to get the product url pages from each
        # search page
        product_search_tasks = [asyncio.ensure_future(search_page_product_urls(soup))]
        for page_num in range(2, page_count + 1):
            fut = search_nth_page_product_urls(session, product_name, page_num)
            product_search_tasks.append(asyncio.ensure_future(fut))

        print()
        print("Retrieving product urls")

        # run all futures concurrently
        product_urls = [url for urls in await gather(*product_search_tasks) 
                        for url in urls]

        print("Retrieved {count} product urls".format(count=len(product_urls)))

        return product_urls

async def get_product(session, product):
    # get the product's page
    async with session.get(product.url) as response:
        
        # find the table of spec data
        soup = BeautifulSoup(await response.text(), "html.parser")
        specs_table = soup.find("div", {"class": "specs-table"})

        # read the key/val pairs, add them to the product
        specs = {}
        if specs_table:
            elements = specs_table.find_all("div", {"class": "border-bottom"})
            for i in range(0, len(elements), 2):
                product.add_spec(elements[i], elements[i+1].get_text())
        return product

# given a product name, asynchronously get specs for all products associated
# with that name
async def get_products(session, product_name):
    # get the product urls from the search pages
    product_urls = await search_product_urls(session, product_name)

    # create a list of futures to get the product specs from each url
    product_spec_tasks = []
    for name, url in product_urls:
        fut = get_product(session, Product(name, url))
        product_spec_tasks.append(asyncio.ensure_future(fut))

    print()
    print("Retrieving product specs")

    # run all futures concurrently
    products = list(await gather(*product_spec_tasks))

    return products

def create_table(db, products):
    # calculate all specs that appear in at least one product
    spec_names = [x + " INTEGER" if "Num" in x else x for x in functools.reduce(
            lambda a,b: a.union(b), 
            [set(prod.all_specs().keys()) for prod in products])]

    # create a table to hold all the specs
    create_stmt = "CREATE TABLE {}({});".format(
        TABLE_NAME,
        ",".join(["Name"] + spec_names)
    )
    db.execute(create_stmt)

    # add each product as a row into the table
    for product in products:
        all_specs = product.all_specs()
        keys = ["Name"] + list(all_specs.keys())
        vals = [product.name] + list(all_specs.values())
        insert_stmt = "INSERT INTO {} ({}) VALUES({});".format(
                TABLE_NAME,
                ",".join(keys),
                ",".join(["?" for x in vals])
        )
        db.execute(insert_stmt, vals)

def interactive(products):
    # get specs
    spec_names = functools.reduce(
            lambda a,b: a.union(b), 
            [set(prod.specs.keys()) for prod in products])

    print()
    print("Retrieved specs: ")

    # print all specs
    for x in spec_names:
        print(" - " + x)

    db = sqlite3.connect(":memory:")
    create_table(db, products)

    print()
    print("Use SQL commands in the table:", TABLE_NAME);

    # run SQL statements
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
    gather = tqdm_asyncio.gather
    product_name = input("Product Name: ")
    asyncio.run(run(product_name))
