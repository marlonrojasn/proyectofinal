import streamlit as st
import pandas as pd
import io
import matplotlib.pyplot as plt
import seaborn as sns

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


        st.subheader("Ítem 2: Clasificación de variables")

        st.write(
            "En este ítem se clasifican las variables del dataset en "
            "numéricas y categóricas. Para realizar esta clasificación "
            "se utiliza una función personalizada que analiza el tipo "
            "de dato de cada variable."
        )

        def clasificar_variables(dataframe):

            numericas = []
            categoricas = []

            for columna in dataframe.columns:

                if pd.api.types.is_numeric_dtype(dataframe[columna]):
                    numericas.append(columna)

                else:
                    categoricas.append(columna)

            return numericas, categoricas

        variables_numericas, variables_categoricas = clasificar_variables(df)

        st.write("Variables numéricas")

        st.write(
            f"Cantidad de variables numéricas: "
            f"{len(variables_numericas)}"
        )

        st.dataframe(
            pd.DataFrame({
                "Variable": variables_numericas
            })
        )

        st.write("Variables categóricas")

        st.write(
            f"Cantidad de variables categóricas: "
            f"{len(variables_categoricas)}"
        )

        st.dataframe(
            pd.DataFrame({
                "Variable": variables_categoricas
            })
        )

        st.write("Conteo de variables")

        conteo_variables = pd.DataFrame({
            "Tipo de variable": [
                "Numéricas",
                "Categóricas"
            ],
            "Cantidad": [
                len(variables_numericas),
                len(variables_categoricas)
            ]
        })

        st.dataframe(conteo_variables)


        st.subheader("Ítem 3: Estadísticas descriptivas")

        st.write(
            "En este ítem se calculan estadísticas descriptivas de las "
            "variables numéricas del dataset. Se analizan medidas como "
            "la media, mediana, desviación estándar, mínimo y máximo."
        )

        st.write("Estadísticas descriptivas")

        estadisticas = df.describe()

        st.dataframe(estadisticas)

        st.write(
            "La media representa el valor promedio de cada variable, "
            "mientras que la mediana corresponde al valor central. "
            "La desviación estándar permite observar la dispersión "
            "de los datos respecto a la media."
        )


        st.subheader("Ítem 4: Análisis de valores nulos")

        st.write(
            "En este ítem se analiza la cantidad de valores nulos "
            "presentes en cada variable."
        )

        nulos = df.isnull().sum()

        tabla_nulos = pd.DataFrame({
            "Variable": nulos.index,
            "Valores nulos": nulos.values
        })

        st.dataframe(tabla_nulos)

        if nulos.sum() > 0:

            nulos_grafico = nulos[nulos > 0]

            fig, ax = plt.subplots(figsize=(10, 5))

            nulos_grafico.plot(
                kind="bar",
                ax=ax
            )

            ax.set_title("Cantidad de valores nulos por variable")
            ax.set_xlabel("Variables")
            ax.set_ylabel("Cantidad de valores nulos")

            plt.xticks(rotation=45, ha="right")

            st.pyplot(fig)

            st.write(
                "Las variables que presentan valores nulos requieren "
                "una revisión antes de realizar análisis posteriores."
            )

        else:

            st.success("El dataset no presenta valores nulos.")


        st.subheader("Ítem 5: Distribución de variables numéricas")

        st.write(
            "En este ítem se analiza la distribución de las variables "
            "numéricas mediante histogramas."
        )

        for columna in variables_numericas:

            fig, ax = plt.subplots(figsize=(8, 4))

            sns.histplot(
                data=df,
                x=columna,
                kde=True,
                ax=ax
            )

            ax.set_title(
                f"Distribución de {columna}"
            )

            ax.set_xlabel(columna)
            ax.set_ylabel("Frecuencia")

            st.pyplot(fig)


        st.subheader("Ítem 6: Análisis de variables categóricas")

        st.write(
            "En este ítem se analizan las variables categóricas mediante "
            "el conteo de sus categorías y gráficos de barras."
        )

        for columna in variables_categoricas:

            st.write(f"Variable: {columna}")

            conteo = df[columna].value_counts(dropna=False)

            tabla_categorias = pd.DataFrame({
                "Categoría": conteo.index.astype(str),
                "Cantidad": conteo.values,
                "Proporción": (
                    conteo.values / len(df)
                ).round(4)
            })

            st.dataframe(tabla_categorias)

            fig, ax = plt.subplots(figsize=(9, 4))

            sns.countplot(
                data=df,
                x=columna,
                ax=ax
            )

            ax.set_title(
                f"Distribución de {columna}"
            )

            ax.set_xlabel(columna)
            ax.set_ylabel("Cantidad")

            plt.xticks(rotation=45, ha="right")

            st.pyplot(fig)


        st.subheader("Ítem 7: Análisis bivariado numérico vs categórico")

        st.write(
            "En este ítem se analiza la relación entre variables numéricas "
            "y la variable Churn. Se comparan variables como MonthlyCharges "
            "y tenure según el estado de abandono del cliente."
        )

        if "Churn" in df.columns:

            variables_bivariado = []

            for columna in ["MonthlyCharges", "tenure"]:

                if columna in df.columns and pd.api.types.is_numeric_dtype(df[columna]):
                    variables_bivariado.append(columna)

            for columna in variables_bivariado:

                st.write(f"Análisis de {columna} vs Churn")

                fig, ax = plt.subplots(figsize=(8, 5))

                sns.boxplot(
                    data=df,
                    x="Churn",
                    y=columna,
                    ax=ax
                )

                ax.set_title(
                    f"{columna} vs Churn"
                )

                ax.set_xlabel("Churn")
                ax.set_ylabel(columna)

                st.pyplot(fig)

                resumen = df.groupby("Churn")[columna].agg(
                    ["mean", "median", "std"]
                ).reset_index()

                resumen.columns = [
                    "Churn",
                    "Media",
                    "Mediana",
                    "Desviación estándar"
                ]

                st.dataframe(resumen)

            st.write(
                "Los gráficos permiten comparar la distribución de las "
                "variables numéricas entre los clientes que permanecieron "
                "y los que abandonaron el servicio."
            )

        else:

            st.warning(
                "No se encontró la variable Churn en el dataset."
            )


        st.subheader("Ítem 8: Análisis bivariado categórico vs categórico")

        st.write(
            "En este ítem se analiza la relación entre variables categóricas "
            "y la variable Churn mediante tablas de frecuencia y gráficos "
            "de barras."
        )

        if "Churn" in df.columns:

            variables_categoricas_bivariado = []

            for columna in ["Contract", "InternetService"]:

                if columna in df.columns:
                    variables_categoricas_bivariado.append(columna)

            for columna in variables_categoricas_bivariado:

                st.write(f"Análisis de {columna} vs Churn")

                tabla = pd.crosstab(
                    df[columna],
                    df["Churn"]
                )

                st.dataframe(tabla)

                tabla_proporcion = pd.crosstab(
                    df[columna],
                    df["Churn"],
                    normalize="index"
                ) * 100

                st.write("Proporción de Churn por categoría (%)")

                st.dataframe(
                    tabla_proporcion.round(2)
                )

                fig, ax = plt.subplots(figsize=(9, 5))

                tabla.plot(
                    kind="bar",
                    ax=ax
                )

                ax.set_title(
                    f"{columna} vs Churn"
                )

                ax.set_xlabel(columna)
                ax.set_ylabel("Cantidad de clientes")

                plt.xticks(rotation=45, ha="right")

                st.pyplot(fig)

            st.write(
                "Las tablas y gráficos permiten identificar diferencias "
                "en el comportamiento de Churn según las categorías "
                "de cada variable."
            )

        else:

            st.warning(
                "No se encontró la variable Churn en el dataset."
            )


        st.subheader("Ítem 9: Análisis basado en parámetros seleccionados")

        st.write(
            "En este ítem el usuario puede seleccionar variables del "
            "dataset para realizar un análisis dinámico."
        )

        columnas_numericas_validas = [
            columna for columna in df.columns
            if pd.api.types.is_numeric_dtype(df[columna])
        ]

        columnas_categoricas_validas = [
            columna for columna in df.columns
            if not pd.api.types.is_numeric_dtype(df[columna])
        ]

        if len(columnas_numericas_validas) > 0:

            variable_numerica = st.selectbox(
                "Seleccione una variable numérica",
                columnas_numericas_validas
            )

        else:

            variable_numerica = None

        if len(columnas_categoricas_validas) > 0:

            variables_categoricas_seleccionadas = st.multiselect(
                "Seleccione una o más variables categóricas",
                columnas_categoricas_validas
            )

        else:

            variables_categoricas_seleccionadas = []

        if variable_numerica is not None:

            st.write(
                f"Análisis de la variable numérica: "
                f"{variable_numerica}"
            )

            st.write(
                df[variable_numerica].describe()
            )

            fig, ax = plt.subplots(figsize=(8, 4))

            sns.histplot(
                data=df,
                x=variable_numerica,
                kde=True,
                ax=ax
            )

            ax.set_title(
                f"Distribución de {variable_numerica}"
            )

            ax.set_xlabel(variable_numerica)
            ax.set_ylabel("Frecuencia")

            st.pyplot(fig)

        for variable_categorica in variables_categoricas_seleccionadas:

            st.write(
                f"Análisis de {variable_categorica}"
            )

            conteo = df[variable_categorica].value_counts()

            st.dataframe(
                conteo.reset_index(
                    name="Cantidad"
                )
            )

            fig, ax = plt.subplots(figsize=(9, 4))

            sns.countplot(
                data=df,
                x=variable_categorica,
                ax=ax
            )

            ax.set_title(
                f"Distribución de {variable_categorica}"
            )

            ax.set_xlabel(variable_categorica)
            ax.set_ylabel("Cantidad")

            plt.xticks(rotation=45, ha="right")

            st.pyplot(fig)


        st.subheader("Ítem 10: Hallazgos clave")

        st.write(
            "En este ítem se presentan algunos hallazgos principales "
            "obtenidos durante el análisis exploratorio de los datos."
        )

        if "Churn" in df.columns:

            cantidad_clientes = len(df)

            clientes_churn = (
                df["Churn"]
                .astype(str)
                .str.strip()
                .str.lower()
                .eq("yes")
                .sum()
            )

            porcentaje_churn = (
                clientes_churn / cantidad_clientes
            ) * 100

            col1, col2 = st.columns(2)

            with col1:

                st.metric(
                    "Total de clientes",
                    cantidad_clientes
                )

            with col2:

                st.metric(
                    "Tasa de Churn",
                    f"{porcentaje_churn:.2f}%"
                )

            st.write("Distribución general de Churn")

            conteo_churn = df["Churn"].value_counts()

            fig, ax = plt.subplots(figsize=(7, 4))

            conteo_churn.plot(
                kind="bar",
                ax=ax
            )

            ax.set_title("Distribución de Churn")
            ax.set_xlabel("Churn")
            ax.set_ylabel("Cantidad de clientes")

            plt.xticks(rotation=0)

            st.pyplot(fig)

            st.write("Principales insights")

            st.write(
                f"1. El dataset contiene {cantidad_clientes} clientes "
                f"analizados."
            )

            st.write(
                f"2. La tasa general de abandono de clientes es "
                f"{porcentaje_churn:.2f}%."
            )

            if "tenure" in df.columns:

                promedio_tenure = df.groupby("Churn")["tenure"].mean()

                st.write(
                    "3. La variable tenure permite comparar la antigüedad "
                    "promedio de los clientes según su estado de Churn."
                )

                st.dataframe(
                    promedio_tenure.reset_index(
                        name="Antigüedad promedio"
                    )
                )

            if "MonthlyCharges" in df.columns:

                promedio_cargos = df.groupby("Churn")[
                    "MonthlyCharges"
                ].mean()

                st.write(
                    "4. MonthlyCharges permite comparar el cargo mensual "
                    "promedio entre los diferentes grupos de Churn."
                )

                st.dataframe(
                    promedio_cargos.reset_index(
                        name="Cargo mensual promedio"
                    )
                )

            st.write(
                "Estos hallazgos permiten identificar patrones iniciales "
                "relacionados con el abandono de clientes y sirven como "
                "base para análisis posteriores."
            )

        else:

            st.warning(
                "No se encontró la variable Churn en el dataset."
            )
