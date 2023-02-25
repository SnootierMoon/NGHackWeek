#TODO: find the actual spec number, not just the string 
#TODO: find name of item (easier to do in getlinks) 
import requests
from bs4 import BeautifulSoup
import re

def fix_spec_name(spec_name):
    return re.sub("[^a-zA-Z_0-9]+", "_", spec_name).strip('_').lower()

class Product:
    def __init__(self, name, url, specs):
        self.name = name
        self.url = url
        self.specs = dict([(fix_spec_name(x), y) for x,y in specs.items()])

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
