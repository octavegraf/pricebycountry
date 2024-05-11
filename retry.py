import vpn_tester

import requests
from bs4 import BeautifulSoup
import sys
import time

# Only executing when a BeautifulSoup Error apperaing

def retry_everything(computer_os, wait, openvpn_file, openvpn_file_path, url, selector_name, selector) :
    print("An error appeared. Retrying.")
    vpn_tester.vpn_disconnect(computer_os, openvpn_file)
    time.sleep(wait)
    vpn_tester.vpn_connect(computer_os, openvpn_file ,openvpn_file_path)
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        return retry_everything(computer_os, wait, openvpn_file, openvpn_file_path, url, selector_name, selector)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        if selector == "class":
                selector_name_tag = soup.find(class_=selector_name)
        elif selector == "id":
                selector_name_tag = soup.find(id=selector_name)

        if selector_name_tag:
            selector_name_text = selector_name_tag.get_text().strip()
            return selector_name_text
        else:
            print("Class or id not found on the page")
            sys.exit(1)

    else:
        print("Failed. Leaving.")
        sys.exit(1)
