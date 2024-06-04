# Ce code source vous est fourni à but éducatif. Vous êtes responsable de son utilisation.

import requests

url = "https://codeavecjonathan.com/scraping/recette/"

response = requests.get(url)
response.encoding = response.apparent_encoding

if response.status_code == 200:
    html = response.text
    # print(html)

    f = open("recette.html", "w")
    f.write(html)
    f.close()

else:
    print("ERREUR:", response.status_code)


print("FIN")
