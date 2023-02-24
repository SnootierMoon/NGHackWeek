
import requests
from bs4 import BeautifulSoup

#from getlinks import urls

class Product:
    def __init__(self, name, url, specs):
        self.name = name
        self.url = url
        self.specs = specs

products = []
urls = ["https://satsearch.co/products/tensortech-cmg-40m-control-moment-gyroscope"]
for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    divs = soup.find('div', {'class': 'specs-table'}).find_all('div', string=True)

    print(divs)






    
