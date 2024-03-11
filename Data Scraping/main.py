import pandas as pd
import time
import csv

from Funktionen_Scraping import anzahl_pages
from Funktionen_DataFrame import concat_dfs

def main(marken_main):
    BASE_URL = "https://www.fatsecret.de/Kalorien-Ern%C3%A4hrung/search?q="
    df = pd.DataFrame(columns= ["Name", "Einheit (g / Stück)","Kalorien", "Fett", "Kohlenhydrate", "Eiweiß", "Marke"])

    for index, mar in enumerate(marken_main):
        print(index+1,"/",len(marken_main))
        print(mar)
        pages = anzahl_pages(mar, BASE_URL)
        print(pages)
        time.sleep(2)
        if pages >= 0:
            df_1 = concat_dfs(mar, pages, BASE_URL)
            df = pd.concat([df, df_1], ignore_index= True)
            time.sleep(2)

    return df

# CSV mit Markennamen einlesen
csv_file = "liste_marken_super.csv"
data = []

with open(csv_file, mode='r') as file:
    csv_reader = csv.reader(file)
    for row in csv_reader:
        data.append(row)

# Daten aus CSV in richtiges Format bringen
data_2 = []
for datenpunkt in data:
    for d in datenpunkt:
        data_2.append(d)

# Daten scrapen und gestaffelt in CSV exportieren
#daten_1 = data_2[:500]
#df_500 = main(daten_1)
#csv_dataframe_1 = "dataframe_500.csv"
#df_500.to_csv(csv_dataframe_1, index = False)

daten_2 = data_2[500:1000]
df_1000 = main(daten_2)
csv_dataframe_2 = "dataframe_1000.csv"
df_1000.to_csv(csv_dataframe_2, index = False)

daten_3 = data_2[1000:1500]
df_1500 = main(daten_3)
csv_dataframe_3 = "dataframe_1500.csv"
df_1500.to_csv(csv_dataframe_3, index = False)

daten_4 = data_2[1500:2000]
df_2000 = main(daten_4)
csv_dataframe_4 = "dataframe_2000.csv"
df_2000.to_csv(csv_dataframe_4, index = False)

daten_5 = data_2[2000:2500]
df_2500 = main(daten_5)
csv_dataframe_5 = "dataframe_2500.csv"
df_2500.to_csv(csv_dataframe_5, index = False)

daten_6 = data_2[2500:3000]
df_3000 = main(daten_6)
csv_dataframe_6 = "dataframe_3000.csv"
df_3000.to_csv(csv_dataframe_6, index = False)

daten_7 = data_2[3000:3500]
df_3500 = main(daten_7)
csv_dataframe_7 = "dataframe_3500.csv"
df_3500.to_csv(csv_dataframe_7, index = False)

daten_8 = data_2[3500:4000]
df_4000 = main(daten_8)
csv_dataframe_8 = "dataframe_4000.csv"
df_4000.to_csv(csv_dataframe_8, index = False)

daten_9 = data_2[4000:]
df_4500 = main(daten_9)
csv_dataframe_9 = "dataframe_4500.csv"
df_4500.to_csv(csv_dataframe_9, index = False)
