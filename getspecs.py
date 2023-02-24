#TODO: find the actual spec number, not just the string 
#TODO: find name of item (easier to do in getlinks) 
import requests
from bs4 import BeautifulSoup

class Product:
        def __init__(self, name, url, specs):
            self.name = name
            self.url = url
            self.specs = specs

def get_products(urls):
    products = []

    for url in urls:
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        divs = soup.find('div', {'class': 'specs-table'}).find_all('div', {'class': 'border-bottom'})

        specs = {}
        for i in range(0, len(divs), 2):
            specs[divs[i].get_text()] = divs[i+1].get_text() #fix
        
        products.append(Product(url, url, specs))
    
    return products
    
def main():
    urls = ["https://satsearch.co/products/tensortech-cmg-40m-control-moment-gyroscope", 
            "https://satsearch.co/products/tensortech-cmg-20m-control-moment-gyroscope",
            "https://satsearch.co/products/berlin-space-tech-rwa05"]
    
    products = get_products(urls)

    for p in products: 
        print(p.name, p.specs)


if __name__ == "__main__":
    main()
        
        








    
