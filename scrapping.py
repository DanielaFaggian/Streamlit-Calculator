import streamlit as st
from requests_html import HTMLSession
import pandas as pd
from bs4 import BeautifulSoup
import numpy as np


def eliminar_cadena_sobrante(df,columna,cadena):
    df[columna] = df[columna].str.replace(cadena,"")
    
def procesar_url(url):
    response = HTMLSession().get(url)
    content = response.html.html
    soup = BeautifulSoup(content,"html.parser")
    return soup.find_all("div", class_="contenido-anuncio")

def DfNew (marca):
    marcas = list()
    precios = list()
    combustibles = list()
    annos = list()
    kms = list()
    cvs = list()
    provincias = list()
    pagina_actual = 1
    marcas_corregir = {'alfa' : 'alfa-romeo',
                       'aston' : 'aston-martin',
                       'lynk' : 'link-co'}
    marca_url = marca.lower()
    if marca_url in marcas_corregir:
        marca_url = marcas_corregir[marca_url]
        
        
        
    processing = st.progress(0)
    percentage = 0
        
    for i in range(1, 8):
        percentage += 13
        processing.progress(percentage)
        url = f"https://www.autocasion.com/coches-segunda-mano/{marca_url}-ocasion?sort=updated_at&direction=desc&page={i}"
        coches_pagina_actual =0
        coches = procesar_url(url)
        
        if len(coches) == 0 and pagina_actual == 1:
            url = f"https://www.autocasion.com/coches-segunda-mano/{marca_url}-1-ocasion?sort=updated_at&direction=desc&page={i}"
            coches = procesar_url(url)
            
        pagina_actual += 1
        
        for coche in coches:
            coches_pagina_actual += 1
            #marca = coche("h2")[0].text.split(" ")[2]
            precio = coche("span")[0].text
        
            datos = coche("ul")
            a = datos[0].get_text().split("\n")
            b = []
            for elem in a:
                if elem:
                    b.append(elem)
            if len(b)!=6:
                continue
            combustible = b[0]
            anno = b[1]
            km = b[2]
            cv = b[3]
            provincia = b[4]
    
            #Appends
            marcas.append(marca)
            precios.append(precio)
            combustibles.append(combustible)
            annos.append(anno)
            kms.append(km)
            cvs.append(cv)
            provincias.append(provincia)
        if coches_pagina_actual<16:
            break
    processing.progress(100)
    df = pd.DataFrame()
    df["Marca"] = marcas
    df["Combustible"] = combustibles
    df["Año"] = annos
    df["Km"] = kms
    df["CV"] = cvs
    df["Provincia"] = provincias
    df["Precio"] = precios
    
    df = df.replace("",np.nan)
    df.dropna(inplace = True)

    if len(df) == 0:
        return f"No se encontraron coches de la marca {marca}"
    eliminar_cadena_sobrante(df,"Km","km")
    eliminar_cadena_sobrante(df,"CV","cv")
    eliminar_cadena_sobrante(df,"Precio","€")
    
    df.reset_index(drop = True, inplace = True)
    
    df = df[["Marca", "Combustible", "Año", "Km", "CV", "Provincia", "Precio"]].applymap(lambda x: x.strip())
    df[["Km", "Precio"]] = df[["Km", "Precio"]].applymap(lambda x: x.replace(".", ""))
    df[["Año", "Km", "CV", "Precio"]] = df[["Año", "Km", "CV", "Precio"]].applymap(lambda x: int(x))
    
    if len(df) == 0:
        return f"No se encontraron coches de la marca {marca}"
    else:
        return df.head(100)
        