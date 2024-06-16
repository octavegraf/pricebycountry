import os
import subprocess
from pathlib import Path

def vpn_connect(computer_os, openvpn_file ,openvpn_file_path):
    if os.path.isfile(openvpn_file_path) and openvpn_file.endswith(".ovpn"):
        if computer_os == "linux":
            subprocess.call(['sudo', 'openvpn', '--config', openvpn_file_path])
        elif computer_os == "macos":
            subprocess.call(['tunblkctl', 'connect', '--wait', Path(openvpn_file).stem])
    print("Connected to", openvpn_file)


def vpn_disconnect(computer_os, openvpn_file):
    if computer_os == "linux":
        subprocess.call(['killall', 'openvpn'])
    elif computer_os == "macos":
        subprocess.call(['tunblkctl', 'disconnect'])
    print("Disconnected from", openvpn_file)