import requests
from bs4 import BeautifulSoup


url = "https://codeavecjonathan.com/scraping/recette_js/"

# Procédé anti détection de script
HEADERS = {"User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36"}

def get_text_if_not_none(e):
    if e:
        return e.text.strip()
    return None


# Seul utilisation de HEADER
response = requests.get(url, headers=HEADERS)
response.encoding = response.apparent_encoding

if response.status_code == 200:
    html = response.text
    # print(html)

    f = open("recette.html", "w")
    f.write(html)
    f.close()

    soup = BeautifulSoup(html, 'html5lib')

    titre = soup.find("h1").text
    print(titre)

    # description = soup.find("p", class_ = "description").text
    description = get_text_if_not_none(soup.find("p", class_ = "description"))
    print(description)

# Ingredients
    #recuperation des elements de la section div du body
    div_ingredients = soup.find("div", class_="ingredients")
    e_ingredients = div_ingredients.find_all("p")
    for e_ingredient in e_ingredients:
        print("INGREDIENT",e_ingredient.text)

# Preparation
    #recuperation des elements de la section div du body
    table_preparations = soup.find("table", class_="preparation")
    e_preparations = table_preparations.find_all("td", class_="preparation_etape")
    for e_preparation in e_preparations:
        print("PREPARATION",e_preparation.text)

else:
    print("Erreur:", response.status_code)    








print("FIN")









