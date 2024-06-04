# Ce code source vous est fourni à but éducatif. Vous êtes responsable de son utilisation.

import requests
from bs4 import BeautifulSoup

url = "https://codeavecjonathan.com/scraping/recette_ua/"

HEADERS = { "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" }


def get_text_if_not_none(e):
    if e:
        return e.text.strip()
    return None

response = requests.get(url, headers=HEADERS)
response.encoding = response.apparent_encoding

if response.status_code == 200:
    html = response.text
    # print(html)

    f = open("recette.html", "w")
    f.write(html)
    f.close()

    soup = BeautifulSoup(html, "html5lib")

    titre = soup.find("h1").text
    print(titre)

    description = get_text_if_not_none(soup.find("p", class_="description2"))
    print(description)

    
    # Ingrédients
    div_ingredients = soup.find("div", class_="ingredients")
    e_ingredients = div_ingredients.find_all("p")
    for e_ingredient in e_ingredients:
        print("INGREDIENT", e_ingredient.text)

    table_preparation = soup.find("table", class_="preparation")
    e_etapes = table_preparation.find_all("td", class_="preparation_etape")
    for e_etape in e_etapes:
        print("ETAPES", e_etape.text)


else:
    print("ERREUR:", response.status_code)


print("FIN")
