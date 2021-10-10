'''
----------------------------------------------
Python Site Backend Finder  - Quey Development

Creators: NeonTheDev, Cuts, Timanttikuutio

Collaborators: NEXUS#7496

Contact: Cuts#0001, Neon#2928 (neon@neonthe.dev), Timanttikuutio#0001, NEXUS#7496

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
import socket
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

with open("files/config.json", "r") as fp:
    config = json.loads(fp.read())

if '-d' in sys.argv: debug = True
else: debug = False

def checkip():
    badcodes = []
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    while 1:
        try:
            ip = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
            with open("files/ips.txt", "a+") as fp:
                fp.write(ip + "\n")

            try:
                #check = requests.get(f'http://{ip}:80', timeout=1)  # Scan the IP for a HTTP conection.
                check = sock.connect_ex((ip, 80))
                if debug: print(f'HIT! IP: http://{ip}') # MIGHT CRASH
            except requests.exceptions.ConnectionError:  # If the connection is unavailable, pass.
                #check = requests.get(f'https://{ip}:80', timeout=1)
                check = sock.connect_ex((ip, 443))
                if debug: print(f'HIT! IP: https://{ip}') # MIGHT CRASH

            #if str(check.status_code) not in badcodes:  # Checking if its a good response code.
            if check == 0:
                ipinfo(ip)  # Create the embed by calling the ipinfo function.

        except requests.exceptions.ConnectionError:  # If the connection is unavailable, pass.
            pass

        except KeyboardInterrupt:
            sys.exit()

        except Exception as e:  #
            print(e)
            pass

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
        try:
            send_screenshot(f"http://{ip}")

            webhook = discord.Webhook.from_url(random.choice(config["webhooks"]), adapter=discord.RequestsWebhookAdapter(requests.session()))
            webhook.send(
                username='Quey Backend Scanner', 
                avatar_url='https://avatars.githubusercontent.com/u/91619825?s=200&v=4',
                file=discord.File("screenshot.png", filename="screenshot.png"),
                embed=discord.Embed.from_dict({
                    "title": f"SITE SCANNER: {geo.get('query')}",
                    "description": "Site found on this IP.",
                    "fields": [
                        {'name': 'IP', 'value': geo.get("query")},
                        {'name': 'IP Type', 'value': geo.get("ipType")},
                        {'name': 'Hostname', 'value': socket.gethostbyaddr(geo.get('query'))[0]},
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
        except:
            pass

def main():
    print('Thread started!')
    checkip()

if __name__ == '__main__':
    with open('ips.txt', 'w+') as nig: pass
    threads = []
    for k in range(100):
        t = threading.Thread(target=main, daemon=True)
        threads.append(t)
        t.start()
    input('Scanning.')
