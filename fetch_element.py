import requests
from bs4 import BeautifulSoup
import sys

def get_text(url, selector_name, selector):
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        if selector == "class":
            selector_name_tag = soup.find(class_=selector_name)
        elif selector == "id":
            selector_name_tag = soup.find(id=selector_name)
        else:
            print("Not a class or id")
            sys.exit(1)

        if selector_name_tag:
            selector_name_text = selector_name_tag.get_text().strip()
            return selector_name_text
        else:
            print("Class or id not found on the page")
            sys.exit(1)
    else:
        print("Failure : {}".format(response.status_code))
        sys.exit(1)