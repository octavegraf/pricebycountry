import requests
from bs4 import BeautifulSoup
import vpn_tester
import retry
import time

vpn_disconnect = vpn_tester.vpn_disconnect
retry_everything = retry.retry_everything

# Fetch element
def get_text(url, selector_name, selector, computer_os, wait, openvpn_file, openvpn_file_path, retry_vpn):
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
        else:
            return retry_everything(computer_os, wait, openvpn_file, openvpn_file_path, url, selector_name, selector)

        if selector_name_tag:
            selector_name_text = selector_name_tag.get_text().strip()
            return selector_name_text
        else:
            print("Class or id not found on the page.")
            return retry_everything(computer_os, wait, openvpn_file, openvpn_file_path, url, selector_name, selector)
    else:
        print(f"Failed to connect to VPN. Retrying. {retry_vpn} attempts left.")
        retry_vpn -= 1
        if retry_vpn <= 0:
            print("VPN can't connect. Skipping.")
            return "VPN Fail."
        else:
            vpn_tester.vpn_disconnect(computer_os, openvpn_file)
            time.sleep(wait)
            vpn_tester.vpn_connect(computer_os, openvpn_file ,openvpn_file_path)
            get_text(url, selector_name, selector, computer_os, wait, openvpn_file, openvpn_file_path, retry_vpn)
