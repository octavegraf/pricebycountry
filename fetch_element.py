import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import vpn_tester
import retry
import time
import config

vpn_disconnect = vpn_tester.vpn_disconnect
retry_everything = retry.retry_everything

# Fetch element
def get_text_bs(url, selector_name, selector, computer_os, wait, openvpn_file, openvpn_file_path, retry_vpn):
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
            try:
                selector_name_text = selector_name_tag.get_text().strip()
                return selector_name_text
            except TypeError as e:
                return retry_everything(computer_os, wait, openvpn_file, openvpn_file_path, url, selector_name, selector)
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
            get_text_bs(url, selector_name, selector, computer_os, wait, openvpn_file, openvpn_file_path, retry_vpn)

def get_text_selenium(url, cookies, selector_element):
    wait = config.wait
    cta = config.cta
    driver = webdriver.Chrome()
    driver.get(url)
    for cookie in cookies:
        driver.add_cookie(cookie)
    time.sleep(wait)
    driver.get(url)
    time.sleep(wait)
    if cta != "":
        try:
            cta = driver.find_element(By.CSS_SELECTOR, cta)
        except NoSuchElementException:
            pass
        else:
            time.sleep(wait)
            cta.click()
            time.sleep(wait)
    try: 
        elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector_element))
        )
    except TimeoutException as ex:
        print("Class or id not found on the page")
        driver.quit()
        return("Not found.")
    selector_name_text = ""
    for element in elements:
        selector_name_text += element.text + "\n"
    driver.quit()
    return selector_name_text.strip()