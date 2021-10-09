'''
----------------------------------------------
Python Site Backend Finder  - Quey Development

Creators: NeonTheDev, Cuts

Contact: Cuts#0001, Neon#2928 (neon@neonthe.dev)

Please give credits if this code is used.

Streamed live on https://twitch.tv/QueyDev
----------------------------------------------
'''
#Imports
import os
import requests
import random
import time
import threading
import dotenv
import discordwebhook

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

dotenv.load_env()
webhook = discordwebhook.Discord(url=os.getenv('WEBHOOK_URL'))

def createip():
    ip = f"{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}.{random.randint(1,255)}" # Generate the IP to check
    #ip = "157.90.107.165" #check discord cuts
    return(ip)

def checkip():
    badcodes = []
    f = open("files\ips.txt", "a+") # 
    while True:
        try:
            ip = createip() # Call the function to genarate the IP.
            f.write(ip + "\n")
            try:
                check = requests.get(f'http://{ip}:80',timeout=1) # Scan the IP for a HTTP conection.
            except requests.exceptions.ConnectionError: # If the connection is unavailable, pass.
                check = requests.get(f'https://{ip}:80',timeout=1)
            if str(check.status_code) not in badcodes: # Checking if its a good response code.
                ipinfo(ip) # Create the embed by calling the ipinfo function.
        except requests.exceptions.ConnectionError: # If the connection is unavailable, pass.
            pass
        except Exception as e: #
            print(e)
            pass

def send_screenshot(url):
    chromeOptions = Options()
    chromeOptions.add_argument("--headless")
    chromeOptions.add_argument("--window_size=1920,1080")
    chromeOptions.headless = True
        
    driver = webdriver.Chrome("./chromedriver", options=chromeOptions)
    driver.get(url)
    driver.save_screenshot("screenshot.png")# ye
    # does?
def ipinfo(ip):
    geo = requests.get(f'http://extreme-ip-lookup.com/json/{ip}').json()
    ipaddr = "[" + geo['query'] + "]" + "(http://" + geo['query'] + ")"
    webhook.post(
        embeds=[
            {
                "title": f"SITE SCANNER: {ip}",
                "description": "Site found on this IP.",
                "fields": [
                    {'name': 'IP', 'value': ipaddr},
                    {'name': 'IP Type', 'value': geo['ipType']},
                    {'name': 'Country', 'value': geo['country']},
                    {'name': 'City', 'value': geo['city']},
                    {'name': 'Continent', 'value': geo['continent']},
                    {'name': 'Country', 'value': geo['country']},
                    {'name': 'Region', 'value': geo['region']},
                    {'name': 'ISP', 'value': geo['isp']},
                    {'name': 'Org', 'value': geo['org']}
                ],
                "image": {"url": "./screenshot.png"},
                "footer": {
                    "text": "Quey development",
                }
            }
        ]
    )   


def main():
    print("Starting...")
    checkip()


threads = []
for k in range(1):
    t = threading.Thread(target=main)
    threads.append(t)
    t.start()
