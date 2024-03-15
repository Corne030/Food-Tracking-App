import csv
import sqlite3

# Verbindung zur SQLite-Datenbank herstellen
conn = sqlite3.connect('produkte.db')
cursor = conn.cursor()

# Tabelle erstellen
cursor.execute('''CREATE TABLE IF NOT EXISTS produkte_restaurants (
                    Name TEXT,
                    'Einheit (g / Stück)' TEXT,
                    Kalorien REAL,
                    Fett REAL,
                    Kohlenhydrate REAL,
                    Eiweiß REAL,
                    Marke TEXT
                )''')

cursor.execute('''CREATE TABLE IF NOT EXISTS produkte_supermarkt (
                    Name TEXT,
                    'Einheit (g / Stück)' TEXT,
                    Kalorien REAL,
                    Fett REAL,
                    Kohlenhydrate REAL,
                    Eiweiß REAL,
                    Marke TEXT
                )''')

# Daten aus csv einlesen und in Datenbank einfügen

data_resturants = []
with open("dataframe_restaurants.csv") as csvdatei:
    csv_reader_object = csv.DictReader(csvdatei)
    for row in csv_reader_object:
        data_resturants.append(row)

for row in data_resturants:
    cursor.execute("INSERT INTO produkte_restaurants (Name, 'Einheit (g / Stück)', Kalorien, Fett, Kohlenhydrate, Eiweiß, Marke) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (row['Name'], row['Einheit (g / Stück)'], row['Kalorien'], row['Fett'], row['Kohlenhydrate'], row['Eiweiß'], row['Marke']))

data_supermärkte = []
with open("dataframe_bereinigt.csv") as csvdatei:
    csv_reader_object = csv.DictReader(csvdatei)
    for row in csv_reader_object:
        data_supermärkte.append(row)

for row in data_supermärkte:
    cursor.execute("INSERT INTO produkte_supermarkt (Name, 'Einheit (g / Stück)', Kalorien, Fett, Kohlenhydrate, Eiweiß, Marke) VALUES (?, ?, ?, ?, ?, ?, ?)",
                   (row['Name'], row['Einheit (g / Stück)'], row['Kalorien'], row['Fett'], row['Kohlenhydrate'], row['Eiweiß'], row['Marke']))

# Änderungen speichern und Verbindung zur Datenbank schließen
conn.commit()
conn.close()