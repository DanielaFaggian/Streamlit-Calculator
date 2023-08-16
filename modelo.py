import streamlit as st

def Modelo():
    st.write("Esta calculadora es un proyecto que busca implementar un modelo de **:blue[Machine Learning]** para calcular el precio de coches de segunda mano en España aplicando Aprendizaje Supervisado.")
    st.write("La aplicación es el resultado de tratar una serie de datos obtenidos mediante Scrapping de la pagina web [autocasion.com](https://www.autocasion.com), lo cual permitira predecir el precio de un coche en el mercado de segunda mano de acuerdo a criterios tales como tipo de combustible, marca, año de matriculación, entre otros.")
    st.write(" ")
    
    tab1, tab2, tab3, tab4 = st.tabs(["Datos", "Modelos y Métricas", "GridSearchCV", "Nuevos Datos"])
    
    with tab1:
        c1, padding, c2 = st.columns((5,1,15))
        c1.write(" ")
        c1.write(" ")
        c1.write("El conjunto de datos obtenidos se compone de casi cien mil coches; sin embargo, tras un procesamiento de datos que permite eliminar patrones atípicos y valores fuera de rango se obtine el conjunto final de datos a usar.")
        c2.image("Imagenes/fig1.png", caption="Resultados scrapping", use_column_width=True)
        
        st.write(" ")
        st.write("Finalmente se trabaja con 83186 datos, los cuales presentan una baja correlación entre si.  Al ser nuestra variable objetivo el **Precio**, podemos observar la poca dependencia que tiene esta respecto a la **Provincia** o la **Marca** del coche")
        st.image("Imagenes/fig2.png", caption="Correlación entre variables", use_column_width=False)
        st.write(" ")
        
    with tab2:
        st.write("Los datos de trabajo fueron normalizados y distribuidos en dos conjuntos (Entrenamiento y Testeo).  Luego se realizó el ajuste usando los siguientes modelos:")
        padding, c3, padding = st.columns((5,10,5))
        c3.write("* _Multiple Lineal Regression (MLR)_ \n* _Nearest Neighbors Regression (KNR)_ \n* _Support Vector Regression (SVR)_ \n* _Random Forest Regression (RFR)_")
        st.image("Imagenes/fig3.png", use_column_width=True)
        st.write(" ")
        st.write("Para determinar que modelo tiene un mejor rendimiento y así decantarse por uno de ellos, se procede a evaluar tres métricas estadisticas")
        padding, c4, padding = st.columns((1,15,1))
        c4.write("+ _Error Absoluto Medio (MAE)_: Se calcula como un promedio de las diferencias absolutas entre los valores objetivos y las predicciones.  Matemáticamente se calcula mediante la siguiente relación:")
        c4.latex(r'''MAE = \frac{1}{N}\sum_{i=1}^{N}|y_i-\hat{y}_i|''')
        c4.write("+ _Error Cuadrático Medio (MSE)_: Se calcula para cada punto la diferencia cuadrada entre la predicción y el objetivo, para luego promediar los valores.  Matemáticamente se calcula mediante la siguiente relación:")
        c4.latex(r'''MSE = \frac{1}{N}\sum_{i=1}^{N}(y_i-\hat{y}_i)^2''')
        c4.write("+ _R al Cuadrado (R squared)_: Es una métrica estrechamente relacionada con la MSE.  Su valor siempre varia entre infinito negativo y uno.  Un valor cercano a 1 indica que un modelo con error cercano a cero.  Matemáticamente se calcula mediante la siguiente relación:")
        c4.latex(r'''R^2 = 1-\frac{MSE(model)}{MSE(baseline)}''')
        c4.write("donde MSE de la linea base se define como:")
        c4.latex(r'''MSE(baseline) = \frac{1}{N}\sum_{i=1}^{N}(y_i-\bar{y}_i)^2''')
        st.write(" ")
        st.write("Los resultados de las tres métricas para los modelos evaluados, se presentan a continuación:")
        st.image("Imagenes/fig4.png", use_column_width=True)
        st.write("Debido a los bajos valores de MAE y MSE, junto al alto valor de Rsquared, presentados por el Modelo Random Forest Regression (RFR).  Se decide trabajar con este modelo en la calculadora de precios de coches.)")
        st.image("Imagenes/fig5.png", use_column_width=False)
        
    with tab3:
        st.write("Una vez escogido el modelo a trabajar es necesario realizar un **Tuning** a este.  El **Tuning** es un proceso experimental que busca optimizar los parametros de un modelo para maximizar su rendimiento.")
        st.write("Este proceso se realiza para respaldar el mejor desempeño y aunque puede ser muy costoso en tiempo, los resultados garantizan la mayor tasa de rendimiento posible.  Para ello se cuenta con modelos de tuning automatizados, donde una vez definidas las opciones que puede tomar cada parametro del modelo, se evaluan una a una todas las combinaciones posibles.")
        st.write("Entre los modelos de tuning mas populares se encuentra **_GridSearchCV_**.")
        st.image("Imagenes/fig6.png", caption="Codigo para aplicacion GridSearchCV al modelo RFR", use_column_width=True)
        st.image("Imagenes/fig7.png", caption="Resultados aplicacion GridSearchCV al modelo RFR", use_column_width=True)
        
    with tab4:
        st.write("Finalmente y con el modelo optimizado se procedio a evaluar un nuevo grupo de datos; los cuales contenian los mismos parametros que aquellos con los que se habia entrenado el modelo.")
        st.write("Estos parametros son Combustible, Año de Matriculación, Km, Potencia del Motor (CV), Provincia y Marca del coche.")
        st.image("Imagenes/fig8.png", caption="Resultados con datos nuevos para el modelo optimizado", use_column_width=True)