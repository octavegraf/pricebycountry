from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service

import vpn_tester
import time
import config

vpn_disconnect = vpn_tester.vpn_disconnect

# Fetch element
def get_text_selenium(url, cookies, selector_element):
    wait = config.wait
    cta = config.cta
    options = webdriver.ChromeOptions()
    if config.hide_browser == True:
        options.add_argument('--disable-gpu')
        options.add_argument("--headless=new")
    options.add_argument('--disable-extensions')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    try:
        driver.get(url)
    except TimeoutException as e:
        print(F"Chrome Timeout.")
        driver.quit()
        return("Chrome Timeout.")
    if cookies != "":
        for cookie in cookies:
            driver.add_cookie(cookie)
            time.sleep(wait)
            driver.get(url)
    if cta != "":
        time.sleep(wait)
        try:
            cta = driver.find_element(By.CSS_SELECTOR, cta)
        except NoSuchElementException:
            print(F"CTA element : {cta} not found.")
            pass
        else:
            time.sleep(wait)
            cta.click()
            time.sleep(wait)
    time.sleep(wait)
    try:
        elements = WebDriverWait(driver, 10).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector_element))
        )
    except TimeoutException as e:
        print(F"Timeout. ({selector_element})")
        driver.quit()
        return("Timeout")
    selector_name_text = ""
    for element in elements:
        selector_name_text += element.text + "\n"
    driver.quit()
    return selector_name_text.strip()