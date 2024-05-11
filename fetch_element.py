import requests
from bs4 import BeautifulSoup
import sys
import vpn_tester
import retry_everything
import time

vpn_disconnect = vpn_tester.vpn_disconnect

# Fetch element
def get_text(url, selector_name, selector, computer_os, wait, openvpn_file, openvpn_file_path):
    try:
        response = requests.get(url)
    except requests.exceptions.RequestException as e:
        already_worked = True
        return retry_everything(computer_os, wait, openvpn_file, openvpn_file_path, url, selector_name, selector)
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
            print("Class or id not found on the page.")
            return retry_everything(computer_os, wait, openvpn_file, openvpn_file_path, url, selector_name, selector)
    else:
        print("Failed to connect. Retrying.")
        vpn_tester.vpn_disconnect(computer_os, openvpn_file)
        time.sleep(wait)
        vpn_tester.vpn_connect(computer_os, openvpn_file ,openvpn_file_path)
        get_text(url, selector_name, selector, computer_os, wait, openvpn_file, openvpn_file_path)
