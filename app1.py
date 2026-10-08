import streamlit as st
st.title("Proyecto Análisis Churn")

st.sidebar.image("internetjpg.jpg", width=150)

Módulos = st.sidebar.selectbox(
    "Desplegar",
    ["Home", "Carga del Data Set", "Ejercicio 2"])

if Módulos == "Home":

    st.write("Telco Customer Churn")

    st.write("Análisis de la salida de clientes en la empresa Telco")
  
    st.write("Marlon Jerson Rojas Novoa")

    st.write("Año: 2026")

    st.write(
        "Aplicación web desarrollada en Python para realizar cálculos, "
        "registrar resultados históricos y visualizar información mediante "
        "una interfaz interactiva.")

    st.write(
        "Desarrollo de una aplicación interactiva para el procesamiento, "
        "registro y visualización de datos, utilizando Python y Streamlit.")


