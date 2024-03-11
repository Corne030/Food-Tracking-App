import streamlit as st
import pandas as pd
import csv
from datetime import datetime
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(layout="wide")

# DARTEN

# DataFrames
df = pd.read_csv("dataframe_bereinigt.csv")
df_restaurants = pd.read_csv("dataframe_restaurants.csv")
df_gegessen = pd.read_csv("dataframe_track.csv")

# Dictionaries - Erklärung:
# Eiweiß = pro kg Körpergewicht
# Kohlenhydrate = %-Anteil an gesamter Kalorienzufuhr
# Fett = %-Anteil an gesamter Kalorienzufuhr
# Muskelaufbau: Kalorienbedarf an Trainingstagen = Männer + 300-700, Frauen + 200-500
# Abnehmen: Kalorienbedarf = beide - 500-1000 pro Tag

männer = {"Muskelaufbau": {"Kalorien": {"soft": 300, "mittel": 500, "stark": 700}},
          "Abnehmen": {"Kalorien": -750}}                                               # hier nochmal checken

frauen = {"Muskelaufbau": {"Kalorien": {"soft": 200, "mittel": 350, "stark": 500}}, 
          "Abnehmen": {"Kalorien": -750}}                                               # hier nochmal checken 

gender_same = {"Muskelaufbau":{"Eiweiß": 1.6, "Kohlenhydrate": 0.55, "Fett": 0.275},    # hier nochmal checken
               "Abnehmen": {"Eiweiß": 1.6, "Kohlenhydrate": 0.55, "Fett": 0.275},       # hier nochmal checken
               "Gewicht halten": {"Eiweiß": 1.6, "Kohlenhydrate": 0.55, "Fett": 0.275}} # hier nochmal checken

aktivitätsfaktor = {"sehr gering": 1.2, "gering": 1.375, "moderat": 1.55, "hoch": 1.725, "sehr hoch": 1.9} # 'sehr hoch' hier vernachlässigt

# SIDEBAR
with st.sidebar:

    st.title("Angabe persönliche Informationen")

    geschlecht = st.radio(
        "Was ist dein Geschlecht?",
        ("Männlich", "Weiblich"))
    
    alter = st.number_input(
        "Gib dein Alter an", min_value = 18, max_value = 99, step = 1)

    gewicht = st.slider(
        "Wie viel wiegst du in kg?",
        40, 150)
    
    groeße = st.slider(
        "Wie groß bist du in cm?",
        140, 220)

    ziel = st.selectbox(
        "Was ist dein Ziel?",
        ("Muskelaufbau", "Gewicht halten", "Abnehmen"))

    aktivität = st.selectbox(
        "Wie aktiv warst du heute (ohne Training)?", 
        ("wenig (nur sitzend)", "etwas (meist sitzend)", "aktiv (viel laufend)", "sehr (harte körperliche Arbeit)"))
    
    # Kalorienbedarf errechnen
    if aktivität == "wenig (nur sitzend)":
        faktor = aktivitätsfaktor["sehr gering"]
    elif aktivität == "etwas (meist sitzend)":
        faktor = aktivitätsfaktor["gering"]
    elif aktivität == "aktiv (viel laufend)":
        faktor = aktivitätsfaktor["moderat"]
    elif aktivität == "sehr (harte körperliche Arbeit)":
        faktor = aktivitätsfaktor["hoch"]

    if geschlecht == "Männlich":
        grundumsatz = 66.47 + (13.7*gewicht) + (5* groeße) - (6.8* alter)
    
    elif geschlecht == "Weiblich":
        grundumsatz = 655.1 + (9.6*gewicht) + (1.8* groeße) - (4.7* alter)

    grundbedarf = grundumsatz*faktor

    if ziel == "Muskelaufbau":
        trainig = st.radio(
            "Ist heute ein Trainingstag?", ("Ja", "Nein"))
        
        gesamtbedarf = grundbedarf
        #st.write(gesamtbedarf)
        
        if trainig == "Ja":
            intensität = st.select_slider(
                "Wie intensiv war dein Trainig?", options = ["soft", "mittel", "stark"])
   
            if geschlecht == "Männlich":
                gesamtbedarf = grundbedarf + männer[ziel]["Kalorien"][intensität]
                #st.write(gesamtbedarf)

            if geschlecht == "Weiblich":
                gesamtbedarf = grundbedarf + frauen[ziel]["Kalorien"][intensität]
                #st.write(gesamtbedarf)

    elif ziel == "Gewicht halten":
        gesamtbedarf = grundbedarf
        #st.write(gesamtbedarf)

    elif ziel == "Abnehmen":
        if geschlecht == "Männlich":
            gesamtbedarf = grundbedarf + männer[ziel]["Kalorien"]
            #st.write(gesamtbedarf)

        if geschlecht == "Weiblich":
            gesamtbedarf = grundbedarf + frauen[ziel]["Kalorien"]
            #st.write(gesamtbedarf)

# TÄGLICHER BEDARF
with st.container():

    st.title("Dein Täglichger Bedarf")

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.subheader("Kalorien")
        st.subheader(round(gesamtbedarf))

    with col2:
        st.subheader("Eiweiß")
        st.subheader(round(gewicht* gender_same[ziel]["Eiweiß"]))

    with col3:
        st.subheader("Kohlenhydrate", help = "Der Anteil von Kohlenhydraten an deinen täglichen Kalorien sollte 45-65% betragen")
        st.subheader(round(gesamtbedarf * gender_same[ziel]["Kohlenhydrate"]))

    with col4:
        st.subheader("Fett", help = "Der Anteil gesunder Fette an deinen täglichen Kalorien sollte 20-35% betragen")
        st.subheader(round(gesamtbedarf * gender_same[ziel]["Fett"]))

# AKTUELLER TAGESSTAND
with st.container():
    
    st.subheader("Aktueller Stand Heute")

    col1, col2, col3, col4 = st.columns(4)

    data_kalo = pd.DataFrame({})
    kalo = []
    kalo.append(round(df_gegessen[df_gegessen['Datum'] == str(datetime.today().date())]['Kalorien'].sum()))
    
    data_eiw = pd.DataFrame({})
    eiw = []
    eiw.append(round(df_gegessen[df_gegessen['Datum'] == str(datetime.today().date())]['Eiweiß'].sum()))
    if ziel == "Muskelaufbau":
        if round(df_gegessen[df_gegessen['Datum'] == str(datetime.today().date())]['Eiweiß'].sum()) >= round(gewicht* gender_same[ziel]["Eiweiß"]):
            st.balloons()
    
    data_kohl = pd.DataFrame({})
    kohl = []
    kohl.append(round(df_gegessen[df_gegessen['Datum'] == str(datetime.today().date())]['Kohlenhydrate'].sum()))
    
    data_fett = pd.DataFrame({})
    fett = []
    fett.append(round(df_gegessen[df_gegessen['Datum'] == str(datetime.today().date())]['Fett'].sum()))
    
    data_kalo["Kalorien"] = kalo
    data_eiw["Eiweiß"] = eiw
    data_kohl["Kohlenhydrate"] = kohl
    data_fett["Fett"] = fett

    

    with col1:
        st.data_editor(data_kalo,column_config={
                "Kalorien": st.column_config.ProgressColumn(
                    "Kalorien",format="%d g", width= "medium",
                    min_value=0,max_value=round(gesamtbedarf),),},hide_index=True,)
        
        if kalo[0] >= gesamtbedarf:
            st.success("Tagesziel erreicht!")
        elif not kalo[0]:
            st.error("Bitte iss etwas!")
        elif kalo[0] < gesamtbedarf and kalo[0] < (gesamtbedarf)*0.8:
            st.warning("Work in progress!")
        elif kalo[0] >= (gesamtbedarf)*0.8:
            st.info("Fast geschafft!")
     
    with col2:
        st.data_editor(data_eiw,column_config={
                "Eiweiß": st.column_config.ProgressColumn(
                    "Eiweiß",format="%d g", width= "medium",
                    min_value=0,max_value=round(gewicht* gender_same[ziel]["Eiweiß"]),),},hide_index=True,)
        
        if eiw[0] >= gewicht* gender_same[ziel]["Eiweiß"]:
            st.success("Tagesziel erreicht!")
        elif not kalo[0]:
            st.error("Bitte iss etwas!")
        elif eiw[0] < gewicht* gender_same[ziel]["Eiweiß"] and eiw[0] < (gewicht* gender_same[ziel]["Eiweiß"])*0.8:
            st.warning("Work in progress!")
        elif eiw[0] >= (gewicht* gender_same[ziel]["Eiweiß"])*0.8:
            st.info("Fast geschafft!")
        
    with col3:
        st.data_editor(data_kohl,column_config={
                "Kohlenhydrate": st.column_config.ProgressColumn(
                    "Kohlenhydrate",format="%d g",width= "medium",
                    min_value=0,max_value=round(gesamtbedarf * gender_same[ziel]["Kohlenhydrate"]),),},hide_index=True,)
        
        if kohl[0] >= gesamtbedarf * gender_same[ziel]["Kohlenhydrate"]:
            st.success("Tagesziel erreicht!")
        elif not kohl[0]:
            st.error("Bitte iss etwas!")
        elif kohl[0] < gesamtbedarf * gender_same[ziel]["Kohlenhydrate"] and kohl[0] < (gesamtbedarf * gender_same[ziel]["Kohlenhydrate"])*0.8:
            st.warning("Work in progress!")
        elif kohl[0] >= (gesamtbedarf * gender_same[ziel]["Kohlenhydrate"])*0.8:
            st.info("Fast geschafft!")
        
    with col4:
        st.data_editor(data_fett,column_config={
                "Fett": st.column_config.ProgressColumn(
                    "Fett",format="%d g",width= "medium",
                    min_value=0,max_value=round(gesamtbedarf * gender_same[ziel]["Fett"]),),},hide_index=True,)
        
        if fett[0] >= gesamtbedarf * gender_same[ziel]["Fett"]:
            st.success("Tagesziel erreicht!")
        elif not fett[0]:
            st.error("Bitte iss etwas!")
        elif fett[0] < gesamtbedarf * gender_same[ziel]["Fett"] and fett[0] < (gesamtbedarf * gender_same[ziel]["Fett"])*0.8:
            st.warning("Work in progress!")
        elif fett[0] >= (gesamtbedarf * gender_same[ziel]["Fett"])*0.8:
            st.info("Fast geschafft!")

# HEUTIGE NAHRUNGSAUFNAHME
with st.container():

    data        = []
    data_liste  = []

    st.subheader("Wie hast du heute gegessen?", help = "Wähle hier aus, ob du heute selber gekocht hast oder auswärts gegessen/bestellt hast.")
    
    tab1, tab2, tab3 = st.tabs(["Selbst gekocht", "Gastronomie", "Manuell hinzufügen"])

    with tab1:

        st.subheader("Was hast du heute gegessen?", help = "Füge hier die Produkte die du gegessen hast hinzu und bestätige deine Eingabe mit einem Klick auf den Button.")
        col1, col2, col3 = st.columns(3)

        namen_produkte = df["Name"]
        namen_produkte = list(set(namen_produkte))
        namen_produkte_sorted = sorted(namen_produkte)

        with col1:
            name = st.selectbox("Name des Produktes", namen_produkte_sorted)

        with col2:
            marke = st.selectbox("Von welcher Marke war das Produkt?", df.loc[df["Name"] == name, "Marke"])
            
        index = df[(df['Name'] == name) & (df['Marke'] == marke)].index[0]

        with col3:
            if (df.loc[index, "Einheit (g / Stück)"]) == "100.0":
                menge = st.number_input("Wie viel hast du gegessen (g/ml) " , min_value = 0)

            elif (df.loc[index, "Einheit (g / Stück)"]) != "100.0":
                menge = st.number_input(f"Wie viel Stück hast du gegessen? (1 Stück = {df.loc[index, "Einheit (g / Stück)"]})" , min_value = 0)

        with col1:
            button = st.button("Eingabe Bestätigen")
            if button:
                if (df.loc[index, "Einheit (g / Stück)"]) == "100.0":
                    
                    data.append(datetime.now().date())
                    data.append(name)
                    data.append(marke)
                    data.append(menge)
                    data.append(df.loc[index, "Kalorien"]/100*menge)
                    data.append(df.loc[index, "Fett"]/100*menge)
                    data.append(df.loc[index, "Kohlenhydrate"]/100*menge)
                    data.append(df.loc[index, "Eiweiß"]/100*menge)
                    data_liste.append(data)
                    
                    for i in data_liste:
                        df_gegessen.loc[len(df_gegessen)] = i

                    df_gegessen.to_csv("dataframe_track.csv", index=False)

                elif (df.loc[index, "Einheit (g / Stück)"]) != "100.0":
                    
                    data.append(datetime.now().date())
                    data.append(name)
                    data.append(marke)
                    data.append(menge)
                    data.append(df.loc[index, "Kalorien"]*menge)
                    data.append(df.loc[index, "Fett"]*menge)
                    data.append(df.loc[index, "Kohlenhydrate"]*menge)
                    data.append(df.loc[index, "Eiweiß"]*menge)
                    data_liste.append(data)
                    
                    for i in data_liste:
                        df_gegessen.loc[len(df_gegessen)] = i

                    df_gegessen.to_csv("dataframe_track.csv", index=False)
                
                st.experimental_rerun()
             
    with tab2:
        st.subheader("Was hast du heute gegessen?", help = "Füge hier die Produkte die du gegessen hast hinzu und bestätige deine Eingabe mit einem Klick auf den Button.")
        
        resturants = df_restaurants["Marke"]
        resturants = list(set(resturants))
        resturants_sort = sorted(resturants)

        col1, col2, col3 = st.columns(3)

        with col1:
            marke_restaurants = st.selectbox("Name des Resturants", resturants_sort)

        with col2:
            name_restaurants = st.selectbox("Wie heißt dein Gericht?", df_restaurants.loc[df_restaurants["Marke"] == marke_restaurants, "Name"])
        
        index_restaurants = df_restaurants[(df_restaurants['Name'] == name_restaurants) & (df_restaurants['Marke'] == marke_restaurants)].index[0]

        with col3:
            if (df_restaurants.loc[index_restaurants, "Einheit (g / Stück)"]) == "100.0" or (df_restaurants.loc[index_restaurants, "Einheit (g / Stück)"]) == "100":
                menge_restaurants = st.number_input("Wie viel hast du gegessen (g/ml)" , min_value = 0)

            elif (df_restaurants.loc[index_restaurants, "Einheit (g / Stück)"]) != "100.0":
                menge_restaurants = st.number_input(f"Wie viel Stück hast du gegessen? (1 Stück = {df_restaurants.loc[index_restaurants, "Einheit (g / Stück)"]})" , min_value = 0)
        
        with col1:
            button_2 = st.button("Eingabe Bestätigen ")
            if button_2:
                if (df_restaurants.loc[index_restaurants, "Einheit (g / Stück)"]) == "100.0" or (df_restaurants.loc[index_restaurants, "Einheit (g / Stück)"]) == "100":
                    
                    data.append(datetime.now().date())
                    data.append(name_restaurants)
                    data.append(marke_restaurants)
                    data.append(menge_restaurants)
                    data.append(df_restaurants.loc[index_restaurants, "Kalorien"]/100*menge_restaurants)
                    data.append(df_restaurants.loc[index_restaurants, "Fett"]/100*menge_restaurants)
                    data.append(df_restaurants.loc[index_restaurants, "Kohlenhydrate"]/100*menge_restaurants)
                    data.append(df_restaurants.loc[index_restaurants, "Eiweiß"]/100*menge_restaurants)
                    data_liste.append(data)
                    
                    for i in data_liste:
                        df_gegessen.loc[len(df_gegessen)] = i

                    df_gegessen.to_csv("dataframe_track.csv", index=False)

                elif (df_restaurants.loc[index_restaurants, "Einheit (g / Stück)"]) != "100.0":
                    
                    data.append(datetime.now().date())
                    data.append(name_restaurants)
                    data.append(marke_restaurants)
                    data.append(menge_restaurants)
                    data.append(df_restaurants.loc[index_restaurants, "Kalorien"]*menge_restaurants)
                    data.append(df_restaurants.loc[index_restaurants, "Fett"]*menge_restaurants)
                    data.append(df_restaurants.loc[index_restaurants, "Kohlenhydrate"]*menge_restaurants)
                    data.append(df_restaurants.loc[index_restaurants, "Eiweiß"]*menge_restaurants)
                    data_liste.append(data)
                    
                    for i in data_liste:
                        df_gegessen.loc[len(df_gegessen)] = i

                    df_gegessen.to_csv("dataframe_track.csv", index=False)
                st.experimental_rerun()

    with tab3:
        st.subheader("Was hast du heute gegessen?")
        st.write("Dein Produkt befindet sich nicht in der Datenbank? Hier kannst du es manuell hinzufügen.")

        produkt = []
        produkt_liste = []
        check = st.radio("Fügst du ein Produkt aus dem Supermarkt hinzu oder eins aus der Gastronomie?",
                          ("Supermarkt", "Gastronomie"))

        col1, col2, col3, col4, col5, col6, col7 = st.columns(7)


        with col1:
            name_manuell = st.text_input("Name Produkt")
        with col2:
            marke_manuell = st.text_input("Marke/Resturant")
        with col3:
            kalorien_manuell = st.number_input("Kalorien", step = 1)
        with col4:
            fett_manuell = st.number_input("Fett", step = 1)
        with col5:
            kohlenhydrate_manuell = st.number_input("Kohlenhydrate", step = 1)
        with col6:
            eiweiß_manuell = st.number_input("Eiweiß", step = 1)
        with col7:
            einheit_manuell = st.text_input("Einheit (g/Stück)", help = "Schau dir die Nähwerttabelle auf der Verpackung deines Produktes an. Wenn die Angaben pro 100g geführt sind, schreibe hier: ***100***. Sind es Angaben pro Stück, schreibe hier die Stückanzahl.")
        
        button_3 = st.button("Produkt hinzufügen")

        if button_3:
            if check == "Supermarkt":
                produkt.append(name_manuell)
                produkt.append(einheit_manuell)
                produkt.append(kalorien_manuell)
                produkt.append(fett_manuell)
                produkt.append(kohlenhydrate_manuell)
                produkt.append(eiweiß_manuell)
                produkt.append(marke_manuell)
                produkt_liste.append(produkt)
                    
                for i in produkt_liste:
                    df.loc[len(df)] = i

                df.to_csv("dataframe_5000.csv", index=False)

            if check == "Gastronomie":
                produkt.append(name_manuell)
                produkt.append(einheit_manuell)
                produkt.append(kalorien_manuell)
                produkt.append(fett_manuell)
                produkt.append(kohlenhydrate_manuell)
                produkt.append(eiweiß_manuell)
                produkt.append(marke_manuell)
                produkt_liste.append(produkt)
                    
                for i in produkt_liste:
                    df_restaurants.loc[len(df_restaurants)] = i

                df_restaurants.to_csv("dataframe_restaurants.csv", index=False)

            st.experimental_rerun()


# DataFrame VERLAUF           
with st.container():

    col1, col2 = st.columns([1.6,1])

    with col1:
        st.subheader("Gesamtverlauf")
        st.dataframe(data = pd.read_csv("dataframe_track.csv"))

    with col2:
        st.subheader("Tagesverglauf")
        
        df_track = pd.DataFrame()
        df_track["Kalorien"] = df_gegessen.groupby('Datum')['Kalorien'].sum()
        df_track["Fett"] = df_gegessen.groupby('Datum')['Fett'].sum()
        df_track["Kohlenhydrate"] = df_gegessen.groupby('Datum')['Kohlenhydrate'].sum()
        df_track["Eiweiß"] = df_gegessen.groupby('Datum')['Eiweiß'].sum()

        st.dataframe(df_track)

        df_track.to_csv("diagramme.csv")



    df_diagramm = pd.read_csv("diagramme.csv")

    with st.expander("Weitere Informationen"):     
        
        # Liniendiagramm
        plt.figure(figsize=(12, 6))
        sns.lineplot(x='Datum', y='Kalorien', data=df_diagramm, label='Kalorien', linewidth=2.5)
        sns.lineplot(x='Datum', y='Fett', data=df_diagramm, label='Fett', linewidth=2.5)
        sns.lineplot(x='Datum', y='Kohlenhydrate', data=df_diagramm, label='Kohlenhydrate', linewidth=2.5)
        sns.lineplot(x='Datum', y='Eiweiß', data=df_diagramm, label='Eiweiß', linewidth=2.5)

        plt.xlabel('Datum')
        plt.ylabel('Nährstoffe')
        plt.title('Verlauf')
        plt.legend()
  
        st.pyplot(plt)


# TO DOS:
# DATEN FÜR ABNEHMEN NOCHMAL ANSCHAUEN
# Daten bereinigen
# sidebar in cache speichern
# Diagramme hinzufügen
# visuell überarbeiten
# test
        
