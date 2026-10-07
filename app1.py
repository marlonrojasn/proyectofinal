import streamlit as st
st.title("Especialización en Python For Analytics")
st.sidebar.markdown(
    "<h2 style='text-align: center;'>Módulos</h2>",
    unsafe_allow_html=True)
Módulos = st.sidebar.selectbox(
    "Desplegar",
    ["Home", "Carga del Data Set", "Ejercicio 2", "Ejercicio 3", "Ejercicio 4"])

if Módulos == "Home":

    st.write("Telco Customer Churn")
    st.image("prog.png", width=300)

    st.write(
        "Análisis de la salida de clientes en la empresa Telco")
  
   st.write("Marlon Jerson Rojas Novoa")

    st.write("Año: 2026")

    st.write(
        "Aplicación web desarrollada en Python para realizar cálculos, "
        "registrar resultados históricos y visualizar información mediante "
        "una interfaz interactiva.")

    st.write(
        "Desarrollo de una aplicación interactiva para el procesamiento, "
        "registro y visualización de datos, utilizando Python y Streamlit.")


