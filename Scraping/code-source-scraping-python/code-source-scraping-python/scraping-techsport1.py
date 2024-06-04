# Ce code source vous est fourni à but éducatif. Vous êtes responsable de son utilisation.

import asyncio
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright

SBR_WS_CDP = 'xxxx' # A remplacer

url = "https://codeavecjonathan.com/scraping/techsport/"

BYPASS_SCRAPING = True

async def run(pw):
    if not BYPASS_SCRAPING:
        print('Connecting to Scraping Browser...')
        browser = await pw.chromium.connect_over_cdp(SBR_WS_CDP)
    try:
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

    finally:
        if not BYPASS_SCRAPING:
            await browser.close()


async def main():
    async with async_playwright() as playwright:
        await run(playwright)


if __name__ == '__main__':
    asyncio.run(main())