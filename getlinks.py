#TODO: find max page of item
#TODO: return an array of Product()'s, with the name and spec field filled
import requests
from getspecs import add_specs, Product
from bs4 import BeautifulSoup

def main():
    product = input("Product Name:")

    url = "https://satsearch.co/products/search/{}".format(product)
    response = requests.get(url)

    soup = BeautifulSoup(response.content, 'html.parser')

    products = []

    search_results = soup.find_all('div', {'class': 'search-results'})[0]

    #p_tag = soup.find_all('a', {'class': 'page-link'})
    search_text = "products found"
    result = soup.find(string=lambda text: search_text in str(text).lower())
    tag = result.parent
    max_results = int(tag.get_text().split()[0])
    page_num = 2

    while True:
        for a in search_results.find_all('a', href=True):
            if "/products/" in a['href']:
                product_url = "https://satsearch.co" + a['href']
                products.append(Product(a.get_text(), product_url, add_specs(product_url)))
        if len(products) < max_results:
            url = "https://satsearch.co/products/search/{}?page={}".format(product, page_num) 
            response = requests.get(url)
            soup = BeautifulSoup(response.content, 'html.parser')
            search_results = soup.find_all('div', {'class': 'search-results'})[0]
            page_num += 1
        else:
            break
    for p in products: 
        print(p.name + ": " + p.url)
        for spec in p.specs:
            print("\t"+spec+": "+p.specs[spec])




    #print(urls)


    '''vendors = []

    for a in soup.find_all('a', href=True):
        if "/url?q=" in a['href']:
            vendor_url = a['href'].split("/url?q=")[1].split("&")[0]
            if "http" in vendor_url:
                vendors.append(vendor_url)

    print("Vendors for {} in {}: ".format(product, area))
    for vendor in vendors:
        print(vendor)'''
if __name__ == '__main__':
    main()