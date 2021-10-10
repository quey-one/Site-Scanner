'''
----------------------------------------------
Python Site Backend Finder  - Quey Development

Creators: NeonTheDev, Cuts, Timanttikuutio

Contact: Cuts#0001, Neon#2928 (neon@neonthe.dev), Timanttikuutio#0001

Please give credits if this code is used.

Streamed live on https://twitch.tv/QueyDev
----------------------------------------------
'''
# Imports
import json
import os
import requests
import random
import time
import threading
import discord
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


with open("files/config.json", "r") as fp:
    config = json.loads(fp.read())


def createip():
    ip = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"  # Generate the IP to check
    #ip = "157.90.107.165" #check discord cuts
    return ip


def checkip():
    badcodes = []
    while True:

        ip = createip()
        print(f"Scanning IP: {ip}\n")

        with open("files/ips.txt", "a+") as fp:
            fp.write(ip + "\n")

        try:
            check = requests.get(f'https://{ip}:80', timeout=1)  # Scan the IP for a HTTP connection.
        except requests.exceptions.ConnectionError:  # If the connection is unavailable, pass.
            pass
        else:
            if str(check.status_code) == "200":  # Checking if its a good response code.
                ipinfo(ip)  # Create the embed by calling the ip info function.


def send_screenshot(url):
    chromeopts = Options()
    chromeopts.add_argument("--headless")
    # chromeopts.add_argument("--window_size=1920,1080")
    chromeopts.headless = True

    driver = webdriver.Chrome("files/chromedriver.exe", options=chromeopts)
    driver.get(url)
    driver.save_screenshot("screenshot.png")


def ipinfo(ip):
    blockedisps = ["Akamai Technologies, Inc.", "Cloudflare, Inc.", "Amazon Technologies Inc.", "Akamai"]
    geo = requests.get(f'http://extreme-ip-lookup.com/json/{ip}').json()
    ipaddr = f"[{geo['query']}](https://{geo['query']})"
    if geo.get("isp") in blockedisps:
        print("Blocked ISP: " + geo.get("isp"))
        pass
    else:
        send_screenshot(f"http://{ip}")

        webhook = discord.Webhook.from_url(random.choice(config["webhooks"]),
                                           adapter=discord.RequestsWebhookAdapter(requests.session()))

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


def main(thread):
    print(f"Starting thread: {thread + 1}")
    checkip()


threads = []
for k in range(config["threads"]):
    t = threading.Thread(target=main, args=(k,))
    threads.append(t)
    t.start()
#the issue is webdriver dm me the error message