from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import unquote
from bs4 import BeautifulSoup
import re
import json
from datetime import datetime
import sqlite3


SITE = 'https://www.avito.ru/'
PAUSE_DURATION = 5

# Отправляем запрос на получение данных и преобразуем данные в json

def get_json(url):
    data = {}

    try:
        service = Service(executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service)
        driver.get(url=url)
        html = driver.page_source

        tree = BeautifulSoup(html, 'html.parser')
        script = tree.find('script', string=re.compile('window.__initialData__'))
        jsontext = script.text.split(';')[0].split('=')[-1].strip()
        undecodedJson = unquote(jsontext)
        data = json.loads(undecodedJson[1:-1])
        
        with open('data.json', 'w', encoding='utf-8') as file:
            json.dump(data, file, ensure_ascii=False)
    except Exception as e:
        print(e)
    finally:
        driver.quit()
    return data
    
# Создаём список из словарей с необходимыми данными объявлений

def get_offers(data):
    offers = []

    for key in data:
        if 'single-page' in key:
            items = data[key]['data']['catalog']['items']
            for item in items:
                if item.get("id"):
                    offer = {}
                    offer["id"] = item["id"]
                    offer["img"] = []
                    for img in item["images"]:
                        offer["img"].append(img["864x648"])
                    offer["img"] = ','.join(offer["img"])
                    offer["title"] = item["title"]
                    offer["url"] = SITE + item["urlPath"]
                    offer["description"] = item["description"]
                    offer["price"] = item["priceDetailed"]["value"]
                    offer["geo"] = item["geo"]["geoReferences"][0]["content"]
                    offer["address"] = item["geo"]["formattedAddress"]
                    
                    timestamp =  datetime.fromtimestamp(item["sortTimeStamp"]/1000)
                    offer["offer_date"] = datetime.strftime(timestamp, '%d.%m.%Y в %H:%M')
                
                    offers.append(offer)
    return offers

# Подключаемся к бд, создаем таблицу и заполняем данными

def check_database(item):
    offer_id = item["id"]
    with sqlite3.connect('db/realty.db') as connection:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT offer_id FROM offers WHERE offer_id = (?)
        """, (offer_id,))
        result = cursor.fetchone()
        if result is None:
            offer = item
            cursor.execute("""
                INSERT INTO offers
                VALUES (NULL, :id, :img, :title, :url, :description, :price, :geo, :address, :offer_date)
            """, offer)
            connection.commit()
            print(f'Объявление {offer_id} добавлено в базу данных')



def main():
   url = 'https://www.avito.ru/vladivostok/kvartiry/sdam/na_dlitelnyy_srok-ASgBAgICAkSSA8gQ8AeQUg?user=1'
   data = get_json(url)
   offers = get_offers(data)
   for item in offers:
       check_database(item)
    

if __name__ == '__main__':
    main()