import requests
from bs4 import BeautifulSoup

def get_text(url, selector_name, selector):
    response = requests.get(url)
    
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        if selector == "class":
            selector_name_tag = soup.find(class_=selector_name)
        elif selector == "id":
            selector_name_tag = soup.find(id=selector_name)
        else:
            return "Not class or id"

        if selector_name_tag:
            selector_name_text = selector_name_tag.get_text().strip()
            return selector_name_text
        else:
            return "Not found"
    else:
        return "Failure : {}".format(response.status_code)

url = 'https://www.spotify.com/fr/premium/'
selector_name = 'Type__TypeElement-sc-goli3j-0 eRmZIa sc-37393cdd-0 VXEqi'
selector = "class"
print(get_text(url, selector_name, selector))
