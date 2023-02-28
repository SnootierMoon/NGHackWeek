import aiohttp, backend, functools, quart, sqlite3, test_products
from collections import Counter

app = quart.Quart(__name__)
db = sqlite3.connect(":memory:")

@app.before_serving
async def before_serving():
    app.client = aiohttp.ClientSession()

@app.after_serving
async def after_serving():
    await app.client.close()

@app.route("/")
async def ep_home():
    return await quart.render_template("home.html")

# create a new database
@app.route("/search")
async def ep_search():
    query = quart.request.args.get("query")

    products = await backend.get_products(app.client, query)

    spec_counter = Counter()
    for product in products:
        for spec in product.specs.keys():
            spec_counter[spec] += 1

    specs = list(functools.reduce(
            lambda a,b: a.union(b), 
            [set(product.specs.keys()) for product in products]))

    common_specs = [spec for spec, _ in spec_counter.most_common()]

    create_stmt = "CREATE TABLE main_tbl({});".format(
        ",".join(["Name", "Url"] + common_specs)
    )

    cur = db.cursor()
    cur.execute("DROP TABLE IF EXISTS main_tbl;")
    cur.execute(create_stmt)
    for product in products:
        keys = ["Name", "Url"] + list(product.specs.keys())
        vals = [product.name, product.url] + list(product.specs.values())
        insert_stmt = "INSERT INTO main_tbl({}) VALUES({});".format(
                ",".join(keys),
                ",".join(["?" for _ in vals])
        )
        cur.execute(insert_stmt, vals)

    db.commit()

    product_names = [{"name": product.name, "url": product.url} 
                     for product in products]

    return await quart.render_template("search.html",
        query=query,
        specs=common_specs,
        products=product_names)


@app.route("/filter")
async def ep_filter():
    arg = quart.request.args
    
    if arg:
        #specs = arg.split(",")
        specs = []
        for item in arg:
            specs.append(item)
        select_stmt = "SELECT Name,Url," + ",".join(specs) + " FROM main_tbl WHERE " + " OR ".join(specs) + ";"

        # TODO: replace with placeholders to avoid injection
        #       the following code does not work
        #select_stmt = "SELECT Name,Url," + ",".join(["?" for _ in specs]) 
        # + " FROM main_tbl WHERE " + " AND ".join(["? IS NOT NULL" for spec in specs]) + ";"
    else:
        specs = []
        select_stmt = "SELECT Name,Url FROM main_tbl;"

    cur = db.cursor()

    products = []
    for row in cur.execute(select_stmt).fetchall():
        products.append({
            "name": row[0],
            "url": row[1],
            "specs": row[2:]
        })

    return { "specs": specs, "products": products }

app.run(debug=True)
