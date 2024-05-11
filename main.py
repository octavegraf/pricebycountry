import config
import fetch_element

import os
from pathlib import Path
import subprocess
import csv
import sys

openvpn = "openvpn/"
computer_os = config.computer_os
website_name = config.website_name 
csv_path = config.csv_path
vpn_name = config.vpn_name
fetched_string = config.fetched_string

# Verifying if OS well configurated
if config != "linux" and config != "macos":
    print("Wrong OS. Please modify config.py")
    sys.exit(1)

# Creating CSV file
with open(csv_path, 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerows([vpn_name, fetched_string])

# Testing every VPN
for openvpn_file in os.listdir(openvpn):
    openvpn_file_path = os.path.join(openvpn, openvpn_file)
    if os.path.isfile(openvpn_file_path) and openvpn_file.endswith(".ovpn"):
        print("Current VPN:", openvpn_file)
        if config == "linux":
            subprocess.call(['sudo', 'openvpn', '--config', openvpn_file_path])
        elif config == "macos":
            subprocess.call(['tunblkctl', 'connect', '--wait', Path(openvpn_file).stem])
        print(fetch_element.get_text(config.url, config.selector_name, config.selector))
        if config == "linux":
            subprocess.call(['killall', 'openvpn'])
        elif config == "macos":
            subprocess.call(['tunblkctl', 'disconnect'])