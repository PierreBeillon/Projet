import requests
from bs4 import BeautifulSoup

url = "http://www.scrapethissite.com/pages/simple/"

def get_text_if_not_none(e):
    if e:
        return e.text.strip()
    return None

response = requests.get(url)

if response.status_code == 200:
    html = response.text
#    print(html)

# Création d'un stockage
    with open("pays.html", "w", encoding="utf-8") as p:
        p.write(html)

        print("Le contenu HTML a été écrit dans le fichier 'pays.html'.")

    soup = BeautifulSoup(html, 'html5lib')

    titre = soup.find("h1").text
    print(titre)

#    lead = soup.find("p", class_ = "lead").text
    lead = get_text_if_not_none(soup.find("p", class_ = "lead"))
    print(lead)


# Pays
    # recuperation des elements de la section div du body
    div_country = soup.find("div", class_="row")
    e_country = div_country.find_all("h3", class_="country-name")
    for e_country in e_country:
        print("Country",e_country.text)

else:
    print("Erreur:", response.status_code)    



print("FIN")




















