'''
----------------------------------------------
Python Site Backend Finder  - Quey Development

Creators: NeonTheDev, Cuts

Contact: Cuts#0001, Neon#2928 (neon@neonthe.dev)

Please give credits if this code is used.

Streamed live on https://twitch.tv/QueyDev
----------------------------------------------
'''
# Imports
import os
import requests
import random
import time
import threading
import dotenv
import discord

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

dotenv.load_dotenv()


webhook = discord.Webhook.from_url(os.getenv('WEBHOOK_URL'), adapter=discord.RequestsWebhookAdapter(requests.session()))


def createip():
    ip = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"  # Generate the IP to check
    # ip = "157.90.107.165" #check discord cuts
    return ip


def checkip():
    badcodes = []
    while True:
        try:
            ip = createip()  # Call the function to genarate the IP.
            with open("files/ips.txt", "a+") as fp:
                fp.write(ip + "\n")
            try:
                check = requests.get(f'http://{ip}:80', timeout=1)  # Scan the IP for a HTTP conection.
            except requests.exceptions.ConnectionError:  # If the connection is unavailable, pass.
                check = requests.get(f'https://{ip}:80', timeout=1)
            if str(check.status_code) not in badcodes:  # Checking if its a good response code.
                ipinfo(ip)  # Create the embed by calling the ipinfo function.
        except requests.exceptions.ConnectionError:  # If the connection is unavailable, pass.
            pass
        except Exception as e:  #
            print(e)
            pass


def send_screenshot(url):
    chromeopts = Options()
    chromeopts.add_argument("--headless")
    # chromeopts.add_argument("--window_size=1920,1080")
    chromeopts.headless = True

    driver = webdriver.Chrome("files/chromedriver", options=chromeopts)
    driver.get(url)
    driver.save_screenshot("screenshot.png")


def ipinfo(ip):
    geo = requests.get(f'http://extreme-ip-lookup.com/json/{ip}').json()
    ipaddr = f"[{geo['query']}](https://{geo['query']})"

    send_screenshot(f"http://{ip}")

    webhook.send(
        file=discord.File("screenshot.png", filename="screenshot.png"),
        embed=discord.Embed.from_dict({
            "title": f"SITE SCANNER: {ip}",
            "description": "Site found on this IP.",
            "fields": [
                {'name': 'IP', 'value': ipaddr},
                {'name': 'IP Type', 'value': geo.get("ipType")},
                {'name': 'Country', 'value': geo.get("country")},
                {'name': 'City', 'value': geo.get("city")},
                {'name': 'Continent', 'value': geo.get("continent")},
                {'name': 'Country', 'value': geo.get("country")},
                {'name': 'Region', 'value': geo.get("region")},
                {'name': 'ISP', 'value': geo.get("isp")},
                {'name': 'Org', 'value': geo.get("org")}
            ],
            "image": {"url": "attachment://screenshot.png"},
            "footer": {
                "text": "Quey development",
            }
        })
    )


def main():
    print("Starting...")
    checkip()


threads = []
for k in range(50):
    t = threading.Thread(target=main)
    threads.append(t)
    t.start()
