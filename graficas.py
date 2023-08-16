import streamlit as st
import plotly.express as px
import pandas as pd
import folium
from folium import plugins
from streamlit_folium import st_folium
from scrapping import DfNew

def Graficas(marca):
    
    #DataFrame datos scrapping
    dfnew = DfNew(marca)
    
    if type(dfnew) == str:
        st.header(f'{dfnew}')
    else:
        with st.expander(label = f"Ultimos coches publicados en la pagina web [autocasion.com](https://www.autocasion.com) de la marca {marca} en España -- (Máximo 100 datos)", expanded = False):
            st.dataframe(dfnew)
    
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["Provincias", "Antigüedad", "Combustibles", "Desgaste", "Precios"])
        
        with tab1:
            # Mapa Provincia
            st.subheader(f"Distribución de coches de la marca {marca} por Provincias")
            st.write("En el mapa puede encontrar información acerca de la cantidad de coches distribuidos por Provincia.")
                        
            df2 = dfnew.groupby(by = "Provincia", as_index = False).count()
            df2.rename(columns={"Marca":"Total"}, inplace =True)
            provincias = pd.read_csv("provincias.csv")
            df_provincias = pd.merge(left = df2, right = provincias, left_on = "Provincia", right_on = "Provincia")
            df_provincias["etiqueta"] = "No hay coches"
            
            for i in range(0, len(df_provincias)):
                df_provincias["etiqueta"][i] = f"Número de coches: {df_provincias['Total'][i]}"
                            
            spain_map = folium.Map(location = [35.51676, -6.27354], zoom_start = 5)
            points = plugins.MarkerCluster()
            
            for lat, lng, prov, label, in zip(df_provincias["latitud"], df_provincias["longitud"], df_provincias["Provincia"], df_provincias['etiqueta']):
                points.add_child(folium.Marker(location = [lat, lng],
                                               icon     = folium.Icon(icon           = "fa-car",
                                                                      icon_color     = "white",
                                                                      color          = "red",
                                                                      prefix         = "fa"),
                                               popup    = f"{prov}\n{label}"))
            spain_map.add_child(points)
            st_folium(fig = spain_map, width = 725)
       
        with tab2:
            # Histograma Año
            st.subheader(f"Antigüedad de los coches de segunda mano de la marca {marca}")
            st.write("Esta representación expone el reparto de coches de segunda mano de acuerdo a su año de matriculación")
            df3 = dfnew.groupby(by = "Año", as_index = False).count()
            df3.rename(columns={"Marca":"Total"}, inplace =True)
            fig_bar1 = px.bar(data_frame = df3,
                             y          = "Total",
                             x          = "Año",
                             color      = "Año",
                             text_auto  = True)
            
            fig_bar1.update_xaxes(title_text = "Año")
            fig_bar1.update_yaxes(title_text = "Total Coches")
            fig_bar1.update_xaxes(categoryorder = "total descending")
            st.plotly_chart(figure_or_data = fig_bar1, use_container_width = True)
            
        with tab3:
            # Pieplot Combustible
            c1, padding, c2 = st.columns((5,1,12))
            df1 = dfnew.groupby(by = "Combustible", as_index = False).count()
            df1.rename(columns={"Marca":"Total"}, inplace =True)
            fig_pie = px.pie(data_frame = df1,
                             names      = "Combustible",
                             values     = "Total")
            c1.write(" ")
            c1.subheader("Distribución coches por Combustible")
            c1.write(" ")
            c1.write(f"En el gráfico de la derecha se puede observar la distribución porcentual de los coches de la marca {marca} respecto al combustible que usan.")
            c2.plotly_chart(figure_or_data = fig_pie, use_container_width = True)
                    
        with tab4:
            # Histograma Km
            st.subheader(f"Desgaste de los coches de segunda mano de la marca {marca}")
            st.write("El histograma muestra la distribución de Kilometros recorridos por el parque automotor de segunda mano")
            hist_fig1 = px.histogram(data_frame = dfnew, x = "Km",  nbins = 50, opacity = 0.8)
            st.plotly_chart(hist_fig1, use_container_width = True)
        
        with tab5:
            # Boxplot Precio
            c3, padding, c4 = st.columns((5,1,12))
            box_fig = px.box(data_frame = dfnew, y = "Precio", width = 400)
            c3.subheader("Distribución estadistica de Precios")
            c3.write(f"En el gráfico de la derecha puede encontrar las estadisticas de Precios para la marca {marca}.")
            c3.write("Ubicando el mouse encima de la figúra obtendra datos tales como máximo, mínimo y media.")
            c4.plotly_chart(box_fig, use_container_width = True)
            
        