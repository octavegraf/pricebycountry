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
csv_line = []

get_text = fetch_element.get_text
new_file = csv_modifier.new_file
add_line = csv_modifier.add_line
vpn_connect = vpn_tester.vpn_connect
vpn_disconnect = vpn_tester.vpn_disconnect

# Verifying if OS well configurated
if computer_os != "linux" and computer_os != "macos":
    print("Wrong OS. Please modify config.py")
    sys.exit(1)

vpn_disconnect(computer_os, "all VPNS.")
time.sleep(wait)

# Creating CSV file
csv_line = [first_column, second_column]
new_file(csv_path, csv_line)



# Listing and sorting all openvpn files
openvpn_folder_list = [f for f in os.listdir(openvpn) if f.endswith('.ovpn')]
openvpn_folder_list_sorted = sorted(openvpn_folder_list)

# Testing every VPN in openvpn folder
for openvpn_file in openvpn_folder_list_sorted:
    openvpn_file_path = os.path.join(openvpn, openvpn_file)
    vpn_connect(computer_os, openvpn_file ,openvpn_file_path)
    fetch_text = ""
    fetch_text = get_text(url, selector_name, selector, computer_os, wait, openvpn_file, openvpn_file_path)
    csv_line = [Path(openvpn_file).stem, fetch_text]
    add_line(csv_path,csv_line)
    vpn_disconnect(computer_os, openvpn_file)
    time.sleep(wait)
