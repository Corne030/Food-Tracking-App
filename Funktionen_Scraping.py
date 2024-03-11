import requests
from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector
import math
import time

def encode_special_characters(url):
    special_characters = {
        "&": "%26",
        "+": "%2B",
        ",": "%2C",
        ";": "%3B",
        "Ä": "%C3%84",
        "Ö": "%C3%96",
        "Ü": "%C3%9C",
        "ä": "%C3%A4",
        "ö": "%C3%B6",
        "ü": "%C3%BC",
        "ß": "%C3%9F",
        " ": "+"
        # Füge hier weitere Sonderzeichen und ihre Kodierungen hinzu
    }

    for char, code in special_characters.items():
        if char in url:
            url = url.replace(char, code)

    return url

def name_produkt(name_produkt):
    '''
    Erhält gescrapte hmtl-Seite.

    Gibt Namen der 10 Produkte pro Seite als Liste wieder.
    '''
    namen = []
    for i in name_produkt:
        name = i.string
        namen.append(name)
    return namen

def nährstoffen_in_zahlen(nährstoffe):
    ein = []
    kal = []
    fet = []
    koh = []
    pro = []

    for i in nährstoffe:
        x = i.text

        einheit = x[x.rfind("pro"):]
        einheit = einheit[:einheit.rfind("-")]
        einheit = einheit[:einheit.rfind("-")]

        if "pro 100g" in einheit:
            einheit = einheit[:einheit.rfind("g")]
            einheit = einheit[einheit.rfind(" "):]
            try:
                einheit = float(einheit)
            except ValueError:
                pass
            ein.append(einheit)
        elif "pro 100ml" in einheit:
            einheit = einheit[:einheit.rfind("m")]
            einheit = einheit[einheit.rfind(" "):]
            try:
                einheit = float(einheit)
            except ValueError:
                pass
            ein.append(einheit)
        else:
            einheit = einheit[:einheit.rfind("(")]
            einheit = einheit[4:]
            ein.append(einheit)

        kalorien = x[x.rfind("Kalorien"):]
        kalorien = kalorien[:14]
        kalorien = kalorien[kalorien.rfind(" "):]
        kalorien = kalorien[:kalorien.rfind("k")]
        try:
            kalorien = float(kalorien)
        except ValueError:
            pass
        kal.append(kalorien)

        fett = x[x.rfind("Fett"):]
        fett = fett[:12]
        fett = fett[:fett.rfind("g")]
        fett = fett[fett.rfind(" "):]
        fett = fett.replace(",", ".")
        try:
            fett = float(fett)
        except ValueError:
            pass
        fet.append(fett)

        kohlh = x[x.rfind("Kohlh"):]
        kohlh = kohlh[:13]
        kohlh = kohlh[:kohlh.rfind("g")]
        kohlh = kohlh[kohlh.rfind(" "):]
        kohlh = kohlh.replace(",", ".")
        try:
            kohlh = float(kohlh)
        except ValueError:
            pass
        koh.append(kohlh)

        eiw = x[x.rfind("Eiw"):]
        eiw = eiw[:12]
        eiw = eiw[:eiw.rfind("g")]
        eiw = eiw[eiw.rfind(" "):]
        eiw = eiw.replace(",", ".")
        try:
            eiw = float(eiw)
        except ValueError:
            pass
        pro.append(eiw)

    return ein, kal, fet, koh, pro

def anzahl_pages(marke, BASE_URL):
    '''
    Scrapen der Anzahl and Seiten dieser Marke.
        Übergabe: gewünschte Marke und BASE_URL
        Ausgabe: Anzahl Seiten der Marke angepasst and die URL
    '''
    
    marke = encode_special_characters(marke)

    url_page = f"{BASE_URL}{marke}"
    #print(url_page)

    while True:
        res = requests.get(url_page)
        
        if res.status_code == 200:
            html = BeautifulSoup(res.text, "html.parser", from_encoding=EncodingDetector.find_declared_encoding(res.content, is_html=True))
            search_result_summary = html.find("div", class_="searchResultSummary")
            
            if search_result_summary:
                time.sleep(0.5)
                
                pages_text = search_result_summary.text
                pages_text = pages_text[pages_text.rfind(" "):].strip()
                
                
                pages = int(pages_text)
                pages = pages / 10
                
                if pages < 1:
                    pages = 0
                elif pages % 1 == 0:
                    pages -= 1
                else:
                    pages = math.floor(pages)
                
                return int(pages)
            
            else:
                print("Kein Element mit der Klasse 'searchResultSummary' gefunden.")
                return -1
        
        else:
            print("Fehler beim Abrufen der URL:", url_page)
            return -1

        if pages is not None:
            break

    return pages