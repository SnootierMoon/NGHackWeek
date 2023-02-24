import requests
from bs4 import BeautifulSoup

product = input("Product Name:")

url = "https://satsearch.co/products/search/{}".format(product)
response = requests.get(url)

soup = BeautifulSoup(response.content, 'html.parser')


urls = []

search_results = soup.find_all('div', {'class': 'search-results'})[0]

p_tag = soup.find_all('a', {'class': 'page-link'})
max_page = int(p_tag[-3].get_text())

for i in range(2,8):
    for a in search_results.find_all('a', href=True):
        if "/products/" in a['href']:
            product_url = a['href']
            urls.append(product_url)
    if i < 7:
        url = "https://satsearch.co/products/search/{}?page={}".format(product, i) 
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')
        search_results = soup.find_all('div', {'class': 'search-results'})[0]

print(len(urls))


    

print(urls)


'''vendors = []

for a in soup.find_all('a', href=True):
    if "/url?q=" in a['href']:
        vendor_url = a['href'].split("/url?q=")[1].split("&")[0]
        if "http" in vendor_url:
            vendors.append(vendor_url)

print("Vendors for {} in {}: ".format(product, area))
for vendor in vendors:
    print(vendor)'''''''''