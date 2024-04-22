from bs4 import BeautifulSoup as bs
import requests
import json

with open("config.json", "r") as file:
    jsonData = json.load(file)

url = jsonData['scraper']['TestURL']

def scrape():
    counter = 0
    data = requests.get(url).text
    soup = bs(data, 'html.parser')
    for item in soup.find_all('img'):
        save_img(item['src'], counter)
        counter += 1

def save_img(url: str, name: str):
    data = requests.get(url).content
    img = open(f'test_images/{name}.jpg', 'wb')
    img.write(data)
    img.close

if __name__ == '__main__':
    scrape()