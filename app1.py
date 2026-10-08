import streamlit as st
import pandas as pd
import io

st.title("Proyecto Análisis Churn")

st.image("imagen1.jpg")

st.sidebar.image("internet.jpg", width=150)

Módulos = st.sidebar.selectbox(
    "Desplegar",
    ["Home", "Carga del Data Set", "Items"]
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

    st.write("Nombre completo: Marlon Jerson Rojas Novoa")
    st.write("Curso / Especialización: Data Science")
    st.write("Año: 2026")

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
        "Python: lenguaje utilizado para el desarrollo del proyecto.\n\n"
        "Pandas: utilizada para la carga, manipulación y análisis de los datos.\n\n"
        "Streamlit: utilizada para desarrollar la aplicación web interactiva.\n\n"
        "Matplotlib / Seaborn: utilizadas para la generación de visualizaciones.\n\n"
        "NumPy: utilizada para operaciones y procesamiento numérico."
    )


elif Módulos == "Carga del Data Set":

    st.header("Carga del Data Set")

    st.write(
        "Seleccione el archivo CSV para cargar "
        "y visualizar la información del dataset."
    )

    archivo = st.file_uploader(
        "Cargar archivo CSV",
        type=["csv"]
    )

    if archivo is not None:

        st.success("El archivo fue cargado correctamente.")

        df = pd.read_csv(archivo, sep=",")

        st.session_state["df"] = df

        st.subheader("Vista previa del Dataset")

        st.dataframe(df.head())

        st.subheader("Dimensiones del Dataset")

        filas, columnas = df.shape

        st.write(f"Filas: {filas}")
        st.write(f"Columnas: {columnas}")

    else:

        st.info("Por favor, cargue un archivo CSV.")


elif Módulos == "Items":

    st.header("Ítems de Análisis")

    if "df" not in st.session_state:

        st.warning(
            "Primero debe cargar un archivo CSV "
            "en el módulo Carga del Data Set."
        )

    else:

        df = st.session_state["df"]

        st.subheader("Ítem 1: Información general del dataset")

        st.write(
            "En este ítem se analiza la estructura general del dataset, "
            "identificando el número de registros, las variables, "
            "los tipos de datos y la cantidad de valores nulos."
        )

        st.write("Información general del dataset")

        buffer = io.StringIO()

        df.info(buf=buffer)

        st.text(buffer.getvalue())

        st.write("Tipos de datos")

        tipos = pd.DataFrame({
            "Variable": df.columns,
            "Tipo de dato": df.dtypes.astype(str).values
        })

        st.dataframe(tipos)

        st.write("Conteo de valores nulos")

        nulos = df.isnull().sum()

        tabla_nulos = pd.DataFrame({
            "Variable": nulos.index,
            "Valores nulos": nulos.values
        })

        st.dataframe(tabla_nulos)

        st.write(f"Total de filas: {df.shape[0]}")
        st.write(f"Total de columnas: {df.shape[1]}")
