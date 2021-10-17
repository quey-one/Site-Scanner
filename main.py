'''
----------------------------------------------
Python Site Backend Finder  - Quey Development
Creators: NeonTheDev, Cuts, Timanttikuutio
Collaborators: NEXUS#7496
Contact: Cuts#0001, Neon#2928 (neon@neonthe.dev), Timanttikuutio#0001, NEXUS#7496
Please give credits if this code is used.
Streamed live on https://twitch.tv/QueyDev

Updated by github.com/psauxx/ <3 
----------------------------------------------
'''

# Imports
import requests, sys, random, threading, discord, socket, selenium, json
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

with open("config.json", "r") as fp:
    config = json.loads(fp.read())

debug = True

def checkip():
    badcodes = []
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(2)
    while 1:
        try:
            ip = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
            with open("Results/ips.txt", "a+") as fp:
                fp.write(ip + "\n")
                with open('Results/ip_working.txt', "a+") as ff:
                    try:
                        check = sock.connect_ex((ip, 80))
                        port = 80
                    except:  
                        check = sock.connect_ex((ip, 443))
                        port = 443
                    if check == 0:
                        print(f"HIT! http://{ip}:{port}")
                        ff.write(ip+'\n')
                        ipinfo(ip, port)
                        
                    
        except (requests.exceptions.ConnectionError, KeyboardInterrupt):  #
            if requests.exceptions.ConnectionError:
                pass
            elif KeyboardInterrupt:
                exit(0)
            pass

def send_screenshot(url):
    chromeopts = Options()
    chromeopts.add_argument("--headless")
    chromeopts.add_experimental_option('excludeSwitches', ['enable-logging'])
    chromeopts.headless = True

    driver = webdriver.Chrome("chromedriver.exe", options=chromeopts)
    driver.get(url)
    driver.save_screenshot("screenshot.png")


def ipinfo(ip, port):
    blockedisps = ["Akamai Technologies, Inc.", "Cloudflare, Inc.", "Amazon Technologies Inc.", "Akamai", "cloudfront", "ERROR: The request could not be satisfied"]
    blocks = ["Invalid", "503"]
    geo = requests.get(f'http://extreme-ip-lookup.com/json/{ip}').json()
    ipaddr = f"[{geo['query']}](https://{geo['query']})"
    if geo.get("isp") in blockedisps:
        print("Blocked ISP: " + geo.get("isp"))
        pass
    else:
        try:
            send_screenshot(f"http://{ip}")
            if port == 443:
                _url = requests.get('https://'+ip).text
            else:
                _url = requests.get('http://'+ip).text
            soup = BeautifulSoup(_url, 'html.parser')
            _tit = "Not found"
            for title in soup.find_all('title'):
                _tit = title.get_text()
            if _tit in blockedisps:
                print("Blocked ISP: " + geo.get("isp"))
                pass
            if _url in blocks:
                print("Blocked: "+ip)
                pass
            webhook = discord.Webhook.from_url(config['webhooks'], adapter=discord.RequestsWebhookAdapter(requests.session()))
            webhook.send(
                username='Quey Backend Scanner', 
                avatar_url='https://avatars.githubusercontent.com/u/91619825?s=200&v=4',
                file=discord.File("screenshot.png", filename="screenshot.png"),
                embed=discord.Embed.from_dict({
                    "title": f"Site Finder",
                    "description": "Site found on this IP.",
                    "fields": [

                        {'name': 'IP', 'value': geo.get("query")},
                        {'name': 'IP Type', 'value': geo.get("ipType")},
                        {'name': 'Hostname', 'value': socket.gethostbyaddr(ip)[0]},
                        {'name': 'IP', 'value': ipaddr+f":{port}"},
                        {'name': 'IP Type', 'value': geo.get("ipType")},
                        {'name': 'Website Title', 'value': _tit},
                        {'name': 'Country', 'value': geo.get("country")},
                        {'name': 'ISP', 'value': geo.get("isp")},
                        {'name': 'Org', 'value': geo.get("org")}
                    ],
                    "image": {"url": "attachment://screenshot.png"},
                    "footer": {
                        "text": "Quey development",
                    },
                    "color": 1127128
                })
            )
            

            
        except:
            pass

def main():
    checkip()

if __name__ == '__main__':
    with open('ips.txt', 'w+') as nig: pass
    threads = []
    for k in range(100):
        t = threading.Thread(target=main, daemon=True)
        threads.append(t)
        t.start()
        
    input('Done Scanning!\n')