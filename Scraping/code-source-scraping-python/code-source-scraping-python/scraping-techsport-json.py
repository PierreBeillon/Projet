# Ce code source vous est fourni à but éducatif. Vous êtes responsable de son utilisation.

import asyncio
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
import json
from datetime import datetime

SBR_WS_CDP = 'xxxx' # A remplacer


# 1 - Liste d'URLs
URLS = [
    "https://codeavecjonathan.com/scraping/techsport/",
    "https://codeavecjonathan.com/scraping/techsport/index.html?id=fitness-pro",
    "https://codeavecjonathan.com/scraping/techsport/index.html?id=solar-sync",
    "https://codeavecjonathan.com/scraping/techsport/index.html?id=tech-wizard"
]

# 2 - Stcockage des données
"""
    Format :

    url
      - title
      - description
      - records
        - date
          - price
          - nb_ratings
"""
JSON_DATA_FILE = "techsport.json"
DATE_TODAY = datetime.today()
DATE_TODAY_STR = DATE_TODAY.strftime('%d-%m-%Y')

BYPASS_SCRAPING = False

def get_text_if_not_none(e):
    if e:
        return e.text.strip()
    return None

def extract_product_page_infos(html):
    infos = {}


    bs = BeautifulSoup(html, "html5lib")
    infos["title"] = get_text_if_not_none(bs.find("span", id="productTitle"))

    infos["nb_ratings"] = 0 # int
    ratings_text = get_text_if_not_none(bs.find("span", id="customer-review-text"))
    if ratings_text:
        nb_ratings_str = ratings_text.split()[0]
        if nb_ratings_str.isdigit():
            infos["nb_ratings"] = int(nb_ratings_str)

    infos["price"] = 0.0 # float
    price_whole_str = get_text_if_not_none(bs.find("span", class_="price-whole"))
    price_fraction_str = get_text_if_not_none(bs.find("span", class_="price-fraction"))
    if price_whole_str and price_whole_str.isdigit():
        price = float(price_whole_str)
        if price_fraction_str and price_fraction_str.isdigit():
            price += float(price_fraction_str)/100
        infos["price"] = price

    infos["description"] = get_text_if_not_none(bs.find("div", id="product-description"))
    



    return infos

async def run(pw):

    # 2.1 - Chargement des données
    all_data = {}

    try:
        f = open(JSON_DATA_FILE, "r")
        json_data = f.read()
        f.close()
        all_data = json.loads(json_data)
    except:
        print("JSON file does not exists")

    if not BYPASS_SCRAPING:
        print('Connecting to Scraping Browser...')
        browser = await pw.chromium.connect_over_cdp(SBR_WS_CDP)
    try:
        i = 0
        for url in URLS:
            i = i+1
            print(f"Page {i}/{len(URLS)}")
            if not BYPASS_SCRAPING:
                page = await browser.new_page()
                print('Connected! Navigating...')
                await page.goto(url)

                await page.screenshot(path="./scraping-browser.png", full_page=True)

                print('Navigated! Scraping page content...')
                html = await page.content()
                # print(html)

                f = open("scraping-browser.html", "w")
                f.write(html)
                f.close()
            else:
                print("Bypass scraping")
                f = open("scraping-browser.html", "r")
                html = f.read()
                f.close()

            # extraire les information à partir de l'html.
            print("Extract infos...")
            infos = extract_product_page_infos(html)
            print(infos)

            # 2.2 - Stockage des données
            if url not in all_data:
                all_data[url] = { "title": infos["title"], "description": infos["description"], "records": {}}
            
            all_data[url]["records"][DATE_TODAY_STR] = {"price": infos["price"], "nb_ratings": infos["nb_ratings"]}

    finally:
        if not BYPASS_SCRAPING:
            await browser.close()

        # 2.3 - Ecriture des données
        f = open(JSON_DATA_FILE, "w")
        json_data = json.dumps(all_data)
        f.write(json_data)
        f.close()


async def main():
    async with async_playwright() as playwright:
        await run(playwright)


if __name__ == '__main__':
    asyncio.run(main())