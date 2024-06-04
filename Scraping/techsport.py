import requests

url = "https://codeavecjonathan.com/scraping/techsport/"

# Procédé anti détection de script
HEADERS = {"User-Agent":"Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36"}


response = requests.get(url, headers=HEADERS)
response.encoding = response.apparent_encoding

if response.status_code == 200:
    html = response.text
    # print(html)

    f = open("techsport.html", "w")
    f.write(html)
    f.close()



else:
    print("Erreur:", response.status_code)    











































