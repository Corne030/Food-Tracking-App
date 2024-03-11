import pandas as pd
import requests
from bs4 import BeautifulSoup
from bs4.dammit import EncodingDetector

from Funktionen_Scraping import name_produkt, nährstoffen_in_zahlen, encode_special_characters

def fill_df(namen, ein, kal, fet, koh, pro):
    '''
    Erstellt einen DataFrame und fügt die übergebenen Daten strukturiert unten in den DataFrame ein.
        Überganbe: Values für alle Spalten des DataFrames ("Name", "Einheit (g / Stück)","Kalorien", "Fett", "Kohlenhydrate", "Eiweiß")
        Ausgabe: Gefüllter DataFrame
    '''
    df = pd.DataFrame(columns= ["Name", "Einheit (g / Stück)","Kalorien", "Fett", "Kohlenhydrate", "Eiweiß"])

    for n, e, k, f, ko, p in zip(namen, ein, kal, fet, koh, pro):
        zeile = []
        zeile.append(n)
        zeile.append(e)
        zeile.append(k)
        zeile.append(f)
        zeile.append(ko)
        zeile.append(p)
        df.loc[len(df)] = zeile

    return df


def seiten_marke(marke, page, BASE_URL):
    '''
    Scrapen der restlichen Seiten.
        Übergabe: gewünschte Marke, Seite und BASE_URL
        Ausgabe: DataFrame einer Seite mit Namen, Nährstoffen und Einheit
    '''    
    marke = encode_special_characters(marke)

    url_rest = f"{BASE_URL}{marke}&pg={page}"
    #print(url_rest)
    res_x = requests.get(url_rest)

    if res_x.status_code == 200:
        html_rest = BeautifulSoup(res_x.text, "html.parser", from_encoding = EncodingDetector.find_declared_encoding(res_x.content, is_html = True))

        nährstoffe = html_rest.find_all("div", class_ = "smallText greyText greyLink")
        namen_produkt = html_rest.find_all("a", class_ = "prominent")

        n = name_produkt(namen_produkt)
        e, k, f, ko, p = nährstoffen_in_zahlen(nährstoffe)

        df = fill_df(n,e,k,f,ko,p)

        return df    
    
def concat_dfs(marke, pages, BASE_URL):
    '''
    Die durch die andere Funktion für jede Seite erstellten DataFrames werden zusammengeführ.
    Zusätzlich wird die Spalte Marke eingefügt und gefüllt.
        Übergabe: Marke, Anzahl Seiten uns BASE_URL
        Ausgabe: DaterFrame aller Produkte einer Marke 
    '''
    df = pd.DataFrame(columns= ["Name", "Einheit (g / Stück)","Kalorien", "Fett", "Kohlenhydrate", "Eiweiß"])

    for page in range(pages+1):
        df_rest = seiten_marke(marke, page, BASE_URL)

        df = pd.concat([df, df_rest], ignore_index= True)

        # hinzufügen der Marke
        df["Marke"] = marke

    return df

