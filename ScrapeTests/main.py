from bs4 import BeautifulSoup as bs
import requests

url = "https://ndawn.info/snow_photos.html"
stakes = []
duds = {
    "Prosper" : [ "https://s3.us-east-2.amazonaws.com/ndawn.info/station_photos/snow/Prosper_NE_SnowStake.jpg", 
                  "https://s3.us-east-2.amazonaws.com/ndawn.info/station_photos/snow/Prosper_South_SnowStake.jpg" ],
    "Fargo" : [ "https://s3.us-east-2.amazonaws.com/ndawn.info/station_photos/snow/Fargo_NE_SnowStake.jpg" ]
}

def scrape():
    check_duds()

    data = requests.get(url).text
    soup = bs(data, 'html.parser')
    for item in soup.find_all('img'):
        if (len(stakes) == 0):
            save_img(item['src'])
            continue
        for name in stakes:
            if name in item['src']:
                save_img(item['src'])
                break
        
def read_stakes():
    file = open('.\ScrapeTests\stakes.txt')
    for line in file:
        if not is_blank(line):
            stakes.append(line.rstrip().lower().capitalize())
    file.close()

def is_blank(line: str) -> bool:
    line = line.replace(" ", "")
    line = line.rstrip()
    return len(line) == 0

def save_img(url: str):
    if (len(url) < 70):
        return
    data = requests.get(url).content
    img = open(f'img/{url[66:]}', 'wb')
    img.write(data)
    img.close

def check_duds():
    for key in duds.keys():
        for name in stakes:
            if key == name:
                for url in duds.get(key):
                    save_img(url)
                stakes.remove(key)

if __name__ == "__main__":
    read_stakes()
    scrape()