import config
import fetch_element
import csv_modifier
import vpn_tester

import os
import sys
from pathlib import Path
import time

openvpn = "openvpn/"

computer_os = config.computer_os
website_name = config.website_name 
url = config.url
selector_name = config.selector_name
selector = config.selector
csv_path = config.csv_path + "/" + website_name + ".csv"
first_column = config.first_column
second_column = config.second_column
wait = config.wait
retry_vpn = config.retry_vpn
cookie = config.cookie
count_lines = 0

get_text = fetch_element.get_text
open_file = csv_modifier.open_file
vpn_connect = vpn_tester.vpn_connect
vpn_disconnect = vpn_tester.vpn_disconnect
count_csv = csv_modifier.count_csv

# Prototyping testing every VPN in openvpn folder
def fetch_everything(url, selector_name, selector, computer_os, wait, retry_vpn, cookie, count_lines):
    count_lines -= 1
    for i in range(count_lines, len(openvpn_folder_list)):
        openvpn_file = openvpn_folder_list[i]
        openvpn_file_path = os.path.join(openvpn, openvpn_file)
        vpn_connect(computer_os, openvpn_file ,openvpn_file_path)
        fetch_text = ""
        fetch_text = get_text(url, selector_name, selector, computer_os, wait, openvpn_file, openvpn_file_path, retry_vpn, cookie)
        csv_line = [Path(openvpn_file).stem, fetch_text]
        open_file(csv_path,csv_line, "a")
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
csv_line = [first_column, second_column]
if os.path.isfile(csv_path):
    count_lines = count_csv(csv_path, "rows")
    if count_lines > 1:
        pass
    else:
        open_file(csv_path, csv_line, "w")
        count_lines = 1
        fetch_everything(url, selector_name, selector, computer_os, wait, retry_vpn, cookie, count_lines)
else:
    open_file(csv_path, csv_line, "w")
    count_lines = 1
    fetch_everything(url, selector_name, selector, computer_os, wait, retry_vpn, cookie, count_lines)


if count_lines < len(openvpn_folder_list):
    while True:
        user_input = input('Does this file completely fetched from different VPN? (y/n)')
        if user_input == "y":
            break
        elif user_input == "n":
            fetch_everything(url, selector_name, selector, computer_os, wait, retry_vpn, cookie, count_lines)
            break
        else:
            print("Invalid input. Please enter y (yes) or n (no).")

count_lines = count_csv(csv_path, "rows")
print(f"Finished fetching websites. File contain {count_lines} rows.")