from bs4 import BeautifulSoup as bs
import requests
import schedule
import time
import json

with open("config.json", "r") as file:
    jsonData = json.load(file)

url = jsonData["scraper"]["URL"]
frequency = jsonData["scraper"]["frequency"]

def scrape():
    data = requests.get(url).text
    soup = bs(data, 'html.parser')
    for item in soup.find_all('img'):
        save_img(item['src'])

def save_img(url: str):
    # This filters out the NDAWN logo in the header of the website
    if (len(url) < 70):
       return
    if (url != "https://s3.us-east-2.amazonaws.com/ndawn.info/station_photos/snow/Amidon_East_SnowStake.jpg"):
        return
    print(url)
    data = requests.get(url).content
    img = open(f'img/{url[66:]}', 'wb')
    img.write(data)
    img.close

if __name__ == '__main__':
    schedule.every(frequency).hours.do(scrape)
    while True:
        schedule.run_pending()
        time.sleep(1)