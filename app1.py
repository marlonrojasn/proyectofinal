import streamlit as st

st.title("Proyecto Análisis Churn")

st.image("imagen1.jpg")

st.sidebar.image("internet.jpg", width=150)

Módulos = st.sidebar.selectbox(
    "Desplegar",
    ["Home", "Carga del Data Set", "Ejercicio 2"]
)

if Módulos == "Home":

    st.header("Telco Customer Churn")

    st.subheader("Objetivo del análisis")

    st.write(
        "El objetivo de este proyecto es analizar la pérdida de clientes "
        "en la empresa Telco (Customer Churn), identificando características "
        "y patrones relacionados con la salida de los clientes. "
        "El análisis permitirá explorar los datos y obtener información "
        "que pueda contribuir a la toma de decisiones."
    )

    st.subheader("Datos del autor")

    st.write("**Nombre completo:** Marlon Jerson Rojas Novoa")
    st.write("**Curso / Especialización:** Data Science")
    st.write("**Año:** 2026")

    st.subheader("Descripción del Dataset")

    st.write(
        "El dataset corresponde a información de clientes de una empresa "
        "de telecomunicaciones. Contiene variables relacionadas con las "
        "características de los clientes, los servicios contratados, "
        "información de facturación y la variable Churn, que indica si "
        "el cliente abandonó o no la empresa."
    )

    st.subheader("Tecnologías utilizadas")

    st.write(
        "• Python: lenguaje utilizado para el desarrollo del proyecto.\n"
        "• Pandas: utilizada para la carga, manipulación y análisis de los datos.\n"
        "• Streamlit: utilizada para desarrollar la aplicación web interactiva.\n"
        "• Matplotlib / Seaborn: utilizadas para la generación de visualizaciones.\n"
        "• NumPy: utilizada para operaciones y procesamiento numérico."
    )
```
