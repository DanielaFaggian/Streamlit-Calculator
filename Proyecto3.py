#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  7 18:00:05 2023

@author: wilmer
"""

import streamlit as st
import pandas as pd
import pickle
import numpy as np
from datos import PAGE_CONFIG
from datos import combustibles
from datos import provincias
from datos import marcas
from graficas import Graficas
from modelo import Modelo

# pip freeze > requirements.txt necesario para tener todas las 
#librerias para usar en github

# En la consola con pip show "libreria" me muestra la version
# de la libreria que estoy usando


st.set_page_config(**PAGE_CONFIG)

columns_names = ["Combustible", "Provincia", "Marca", "Año", "Kms", "CV"]

# Title
st.markdown("<h1 style='text-align: center; color: grey; '>Calculadora precio coches de segunda mano - ESPAÑA</h1>", unsafe_allow_html= True)

tab1, tab2 = st.tabs(["Calculadora", "Modelo"])

with tab1:
    #Explicación
    st.text("")
    st.write("<h4 style='font-weight: 100; font-size: 20px; color: black;'>Esta aplicación usa un modelo de Machine Learning para predecir el precio de un coche de segunda mano en España.</h4>", unsafe_allow_html=True)
    st.write("<h4 style='font-weight: 100; font-size: 20px; color: black;'>Para entender mejor el funcionamiento del modelo y los criterios de validación, dirijase por favor a la pestaña Modelo; ahí se explica de manera detallada como se obtiene el valor calculado por esta aplicación</h4>", unsafe_allow_html=True)
    
    
    with st.form("my_form"):
        st.write("<h4 style='font-weight: 100; font-size: 20px; color: darkblue;'>Por favor ingrese los siguientes datos de su coche para poder calcular el precio</h4>", unsafe_allow_html=True)
        
        # Combustible
        st.header("Combustible")
        combustible = st.radio(label = "Combustible",
                               label_visibility = "hidden",
                          options = combustibles,
                          index = 0,
                          disabled = False,
                          horizontal = True,)
            
        #Columnas
        c1, padding, c2 = st.columns((10,2,10))
        
        # Provincia
        c1.header("Provincia")
        provincia = c1.selectbox("Provincia", label_visibility = "hidden", options = provincias)
        #c1.write(f"Provincia: {choice}")
        
        # Marca
        c2.header("Marca")
        marca = c2.selectbox("Marca", label_visibility = "hidden", options = marcas)
        #c2.write(f"Marca: {choice}")   
         
        # Año
        st.header("Año de Matriculación")
        anio = st.slider(label     = "Año",
                       label_visibility = "hidden",
                       min_value = 1993,
                       max_value = 2023,
                       value     = 2008)
        
        # Kms
        c1.header("Kilometros")
        kms = c1.number_input(label = "Km",
                              label_visibility = "hidden",
                                min_value = 0,
                                max_value = 500000,
                                value = 0,
                                step = 10)
        
        # CV
        c2.header("Potencia (CV)")
        cv = c2.number_input(label = "cv",
                              label_visibility = "hidden",
                                min_value = 50,
                                max_value = 500,
                                value = 50,
                                step = 25)
        
        # Datos del usuario
        data = [combustible, provincia, marca, anio, kms, cv]
        
        df_usuario = pd.DataFrame(data = [data], columns = columns_names)
        #st.dataframe(df_usuario)
        
        # Aplicar LabelEnconder a los datos del usuario
        with open("encoders.sav", "br") as file:
            encoders = pickle.load(file)
        
        df_testeo = df_usuario
        Combustible = encoders["Combustible"].transform(df_testeo["Combustible"])
        Provincia = encoders["Provincia"].transform(df_testeo["Provincia"])
        Marca = encoders["Marca"].transform(df_testeo["Marca"])
        
        df_testeo["Combustible"] = Combustible
        df_testeo["Provincia"] = Provincia
        df_testeo["Marca"] = Marca
        
        X = np.array(df_testeo)
        
        with open("escaladorX1.sav", "br") as file:
            x_scaler = pickle.load(file)
        
        X = x_scaler.transform(X)
        
        with open("modelo_RandomForestRegressor1.sav", "br") as file:
            modelo_final = pickle.load(file)
        
        ynor = modelo_final.predict(X)
        
        with open("escaladory1.sav", "br") as file:
            y_scaler = pickle.load(file)
        y =  y_scaler.inverse_transform(ynor.reshape(-1, 1))
        submitted = st.form_submit_button(label = "Calcular\t :euro:",
                     type  = "primary")
        if submitted:
            st.write(f"<h2 style='font-size: 24px; color: green; '>El precio es de <strong>{round(y[0][0], 2)}</strong> Euros</h2>", unsafe_allow_html=True)
            st.divider()
            st.text("")
            st.write("<h4 style='font-weight: 100; font-size: 20px; color: black;'>A continuación se realiza una busqueda en tiempo real para presentar el estado actual de los coches de su marca en España</h4>", unsafe_allow_html= True)    
            Graficas(marca)

with tab2:
    Modelo()