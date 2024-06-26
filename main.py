import config
import fetch_element
import csv_modifier
import vpn_tester
import chatgpt

import os
import sys
from pathlib import Path
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


openvpn = os.path.join(os.path.dirname(__file__), 'openvpn')

computer_os = config.computer_os
website_name = config.website_name
url = config.url
selector_name = config.selector_name
selector = config.selector
csv_path = os.path.join(os.path.dirname(__file__), 'fetched') + "/" + website_name + ".csv"
first_column = config.first_column
second_column = config.second_column
third_column = config.third_column
fourth_column = config.fourth_column
wait = config.wait
retry_vpn = config.retry_vpn
input_price = config.input_price
output_price = config.output_price
model = config.model
prompt = config.prompt
cookie = config.cookie

get_text_selenium = fetch_element.get_text_selenium
open_file = csv_modifier.open_file
vpn_connect = vpn_tester.vpn_connect
vpn_disconnect = vpn_tester.vpn_disconnect
count_csv = csv_modifier.count_csv
read_element_csv = csv_modifier.read_element_csv
estimated_cost = chatgpt.estimated_cost
get_price_format = chatgpt.get_price_format
add_chatgpt_data = csv_modifier.add_chatgpt_data

# Prototyping testing every VPN in openvpn folder
def fetch_everything(url, selector_name, selector, computer_os, wait, openvpn_folder_list, retry_vpn, count_lines, cookie):
    count_lines -= 1
    if selector == "class":
        selector = "."
    elif selector == "id":
        selector = "#"
    selector_name = selector_name.split()
    selector_element = [selector + selector_word for selector_word in selector_name]
    selector_element = ' '.join(selector_element)
    options = webdriver.ChromeOptions()
    if config.hide_browser == True:
        options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    cookies = cookies_after = cookies_before = ""
    cookies_before = driver.get_cookies()
    if cookie == True:
        confirmation = input("Is the current element present on the page? (y to confirm) ")
        if confirmation.lower() == "y":
            cookies_after = driver.get_cookies()
            cookies = [cookie for cookie in cookies_after if cookie not in cookies_before]
    elif cookie == False:
            cookies = ""
    time.sleep(wait)
    fetch_text = get_text_selenium(url, cookies, selector_element)
    driver.quit()
    lines = fetch_text.split('\n')
    print("Here are the lines of text found on the page:")
    for idx, line in enumerate(lines):
        print(f"{idx+1}: {line}")
    line_number = int(input("Please enter the line number you want to fetch: "))
    while line_number < 1 or line_number > len(lines):
        print("Invalid line number. Please choose a number within the range.")
        line_number = int(input("Please enter the line number you want to fetch: \n"))
    line_number -= 1

    for i in range(count_lines, len(openvpn_folder_list)):
        openvpn_file = openvpn_folder_list[i]
        openvpn_file_path = os.path.join(openvpn, openvpn_file)
        vpn_connect(computer_os, openvpn_file ,openvpn_file_path)
        fetch_text = ""
        fetch_text = get_text_selenium(url, cookies, selector_element)
        lines = fetch_text.split('\n')
        fetch_text = lines[line_number]
        print(F"Text found : {fetch_text}")
        csv_line = [Path(openvpn_file).stem, fetch_text]
        open_file(csv_path,csv_line, "a")
        count_lines += 1
        vpn_disconnect(computer_os, openvpn_file)
        print("—————————————————————————————————")
        time.sleep(wait)

# Verifying if OS well configurated
if computer_os != "linux" and computer_os != "macos":
    print("Wrong OS. Please modify config.py")
    sys.exit(1)

vpn_disconnect(computer_os, "all VPNS.")

# Listing and sorting all openvpn files
openvpn_folder_list = [f for f in os.listdir(openvpn) if f.endswith('.ovpn')]
openvpn_folder_list = sorted(openvpn_folder_list)



# Verifying CSV file
csv_line = [first_column, second_column, third_column, fourth_column]
if os.path.isfile(csv_path):
    count_lines = count_csv(csv_path, "rows")
    if count_lines > 1:
        pass
    else:
        open_file(csv_path, csv_line, "w" )
        count_lines = 1
        fetch_everything(url, selector_name, selector, computer_os, wait, openvpn_folder_list, retry_vpn, count_lines, cookie)
else:
    open_file(csv_path, csv_line, "w")
    count_lines = 1
    fetch_everything(url, selector_name, selector, computer_os, wait, openvpn_folder_list, retry_vpn, count_lines, cookie)

count_lines = count_csv(csv_path, "rows")
if count_lines < len(openvpn_folder_list):
    while True:
        user_input = input('Does this file completely fetched from different VPN? (y/n)')
        if user_input == "y":
            break
        elif user_input == "n":
            fetch_everything(url, selector_name, selector, computer_os, wait, openvpn_folder_list, retry_vpn, count_lines, cookie)
            break
        else:
            print("Invalid input. Please enter y (yes) or n (no).")

count_lines = count_csv(csv_path, "rows")
print(f"Finished fetching websites. File contain {count_lines} rows.")
print("Please verify your file first, and correct errors if there is some.")
count_lines = 1
while count_lines < count_csv(csv_path, "rows"):
    try: 
        read_element_csv(csv_path, count_lines, 3)
        count_lines += 1
    except IndexError:
        print("Price and currency are currently not separated. You can use ChatGPT to generate them in a correct format.")
        lines_remaining = count_csv(csv_path, "rows") - count_lines
        cost = estimated_cost(input_price, output_price, model, prompt, lines_remaining, url)
        print(f"Estimated cost : {cost}$ [DON'T FORGET THAT REAL VALUE CAN BE DIFFERENT]")
        while True:
            user_input = input("Do you want to continue ? (y)")
            if user_input == "y":
                break
            else:
                print("Invalid input. Please enter y (yes).")
        break

while count_lines < count_csv(csv_path, "rows"):
    fetched_content = read_element_csv(csv_path, count_lines, 1)
    chatgpt_response = get_price_format(fetched_content, read_element_csv(csv_path, count_lines, 0))
    print(F"ChatGPT response : {chatgpt_response}")
    add_chatgpt_data(csv_path, count_lines, chatgpt_response)
    count_lines += 1
print("Finished.")