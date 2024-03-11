import requests
from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector
import math
import time
import csv

def anzahl_pages_marken_pro_Buchstabe(BASE_URL_Marken, Buchstabe):
    '''
    Scrapen der Anzahl and Seiten pro Buchstabe.
        Übergabe: BASE_URL und Buchstabe
        Ausgabe: Anzahl Seiten pro Buchstabe angepasst and die URL
    '''

    url_page  = f"{BASE_URL_Marken}f={Buchstabe}&t=3" # 1,2,3 am Ende für Kategorie Hersteller, Restaurant oder Supermarkt

    res = requests.get(url_page)

    if res.status_code == 200:
        html = BeautifulSoup(res.text, "html.parser", from_encoding = EncodingDetector.find_declared_encoding(res.content, is_html = True))

        pages = html.find("div", class_ = "searchResultSummary").text
        pages = pages[pages.rfind(" "):]
        pages = int(pages)
        pages = pages/20
        if pages % 1 == 0 or pages < 1:
            pages = pages-1
        if pages < 0:
            pages = math.ceil(pages)
        else:
            pages = math.floor(pages)
    
    time.sleep(2)
    return pages

def marken(Kategorie):
    '''
    Geht für jeden Buchstaben die Seiten durch und speichert alle Marken in einer Liste (leider verbuggt)
        Ausgabe: Liste aller Marken
    '''
    buchstaben = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z"]
    BASE_URL_Marken = "https://www.fatsecret.de/Default.aspx?pa=brands&"
    namen = []

    for b in buchstaben:
        hilfsliste = []
        pages_buchstaben = anzahl_pages_marken_pro_Buchstabe(BASE_URL_Marken, b)
        print(b, pages_buchstaben)
        time.sleep(2)
        
        for page in range(pages_buchstaben+1):
            url = f"{BASE_URL_Marken}pg={page}&f={b}&t={Kategorie}" # 1,2,3 am Ende für Kategorie Hersteller, Restaurant oder Supermarkt | 
            
            # scrape Marken
            res = requests.get(url)

            if res.status_code == 200:
                html_rest = BeautifulSoup(res.text, "html.parser", from_encoding = EncodingDetector.find_declared_encoding(res.content, is_html = True))

                namen_marken = html_rest.find_all("h2")

                for i in namen_marken:
                    name = i.text
                    name = name[1:]
                    hilfsliste.append(name)
                        
            if len(hilfsliste) >0:
                namen.append(hilfsliste)
                        
    return namen

# erstellen von CSV mit allen Marken, Supermärkten und Resturants

# Marken und Supermärkte (damit gemeint Eigenmarke des Supermarktes), können unter einer Kategorie gefasst werden
liste_marken = marken(1)
csv_marken = "liste_marken.csv"

with open(liste_marken, mode='w', newline='') as file:
    writer = csv.writer(file)
    for row in liste_marken:
        writer.writerow(row)

liste_supermärkte = marken(3)
csv_super = "liste_supermärkte.csv"

with open(liste_supermärkte, mode='w', newline='') as file:
    writer = csv.writer(file)
    for row in liste_supermärkte:
        writer.writerow(row)

# Restaurants müssen separat behandelt werden, da eigene Kategorie
liste_restaurant = marken(2)
csv_restaurant = "liste_restaurants.csv"

with open(csv_restaurant, mode='w', newline='') as file:
    writer = csv.writer(file)
    for row in liste_restaurant:
        writer.writerow(row)
