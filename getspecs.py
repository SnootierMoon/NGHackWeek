#TODO: find the actual spec number, not just the string 
#TODO: find name of item (easier to do in getlinks) 
import requests
from bs4 import BeautifulSoup
import asyncio

class Product:
    def __init__(self, name, url, specs):
        self.name = name
        self.url = url
        self.specs = specs

def add_specs(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

    divs = soup.find('div', {'class': 'specs-table'})
    if divs: 
        divs = divs.find_all('div', {'class': 'border-bottom'})

    specs = {}
    if divs:
        for i in range(0, len(divs), 2):
            specs[divs[i].get_text()] = divs[i+1].get_text() #fix
        
    return specs
        
        
        








    
