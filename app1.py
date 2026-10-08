import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title="Proyecto Análisis Churn",
    layout="wide"
)

st.title("Proyecto Análisis Churn")

try:
    st.image("imagen1.jpg")
except:
    pass

try:
    st.sidebar.image("internet.jpg", width=150)
except:
    pass


# ==================================================
# MENÚ PRINCIPAL
# ==================================================

modulo = st.sidebar.selectbox(
    "Desplegar",
    [
        "Home",
        "Carga del Data Set",
        "Items"
    ]
)


# ==================================================
# HOME
# ==================================================

if modulo == "Home":

    st.header("Telco Customer Churn")

    st.subheader("Objetivo del proyecto")

    st.write(
        "El objetivo del proyecto es analizar el comportamiento de los "
        "clientes de una empresa de telecomunicaciones e identificar "
        "características y patrones relacionados con la pérdida de clientes "
        "(Churn), con la finalidad de generar información útil para la "
        "toma de decisiones."
    )

    st.subheader("Datos del autor")

    st.write("**Nombre completo:** Marlon Jerson Rojas Novoa")
    st.write("**Curso / Especialización:** Data Science")
    st.write("**Año:** 2026")

    st.subheader("Descripción del Dataset")

    st.write(
        "El dataset contiene información relacionada con clientes de una "
        "empresa de telecomunicaciones. Incluye características de los "
        "clientes, servicios contratados, información de facturación y la "
        "variable Churn, que indica si el cliente abandonó o no la empresa."
    )

    st.subheader("Tecnologías utilizadas")

    st.write(
        "Python, Pandas, Streamlit, Matplotlib, Seaborn y NumPy."
    )


# ==================================================
# CARGA DEL DATA SET
# ==================================================

elif modulo == "Carga del Data Set":

    st.header("Carga del Data Set")

    archivo = st.file_uploader(
        "Cargar archivo CSV",
        type=["csv"]
    )

    if archivo is not None:

        try:

            df = pd.read_csv(archivo)

            st.success("Archivo cargado correctamente.")

            st.session_state["df"] = df

            st.subheader("Vista previa")

            st.dataframe(
                df.head(),
                use_container_width=True
            )

            filas, columnas = df.shape

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Número de filas",
                    filas
                )

            with col2:
                st.metric(
                    "Número de columnas",
                    columnas
                )

        except Exception as e:

            st.error(
                f"No se pudo cargar el archivo: {e}"
            )

    else:

        st.info(
            "Cargue un archivo CSV para comenzar el análisis."
        )


# ==================================================
# ITEMS
# ==================================================

elif modulo == "Items":

    # ----------------------------------------------
    # SUBMENÚ DE LOS 10 ITEMS
    # ----------------------------------------------

    item = st.sidebar.selectbox(
        "Seleccionar Item",
        [
            "Ítem 1: Información general",
            "Ítem 2: Clasificación de variables",
            "Ítem 3: Estadísticas descriptivas",
            "Ítem 4: Valores nulos",
            "Ítem 5: Distribución numérica",
            "Ítem 6: Variables categóricas",
            "Ítem 7: Numérico vs categórico",
            "Ítem 8: Categórico vs categórico",
            "Ítem 9: Parámetros seleccionados",
            "Ítem 10: Hallazgos clave"
        ]
    )

    # ----------------------------------------------
    # VERIFICAR DATASET
    # ----------------------------------------------

    if "df" not in st.session_state:

        st.warning(
            "Primero debe cargar el archivo CSV en "
            "'Carga del Data Set'."
        )

    else:

        df = st.session_state["df"]


        # ==========================================
        # ITEM 1
        # ==========================================

        if item == "Ítem 1: Información general":

            st.header("Ítem 1: Información general")

            filas, columnas = df.shape

            col1, col2 = st.columns(2)

            with col1:
                st.metric(
                    "Número de filas",
                    filas
                )

            with col2:
                st.metric(
                    "Número de columnas",
                    columnas
                )

            st.subheader("Información de las variables")

            informacion = pd.DataFrame({
                "Variable": df.columns,
                "Tipo de dato": df.dtypes.astype(str).values,
                "Valores no nulos": df.notnull().sum().values,
                "Valores nulos": df.isnull().sum().values
            })

            st.dataframe(
                informacion,
                use_container_width=True
            )


        # ==========================================
        # ITEM 2
        # ==========================================

        elif item == "Ítem 2: Clasificación de variables":

            st.header("Ítem 2: Clasificación de variables")

            variables_numericas = []
            variables_categoricas = []

            for columna in df.columns:

                if pd.api.types.is_numeric_dtype(
                    df[columna]
                ):

                    variables_numericas.append(columna)

                else:

                    variables_categoricas.append(columna)

            st.subheader("Variables numéricas")

            tabla_numericas = pd.DataFrame({
                "Variable": variables_numericas,
                "Tipo": "Numérica"
            })

            st.dataframe(
                tabla_numericas,
                use_container_width=True
            )

            st.metric(
                "Cantidad de variables numéricas",
                len(variables_numericas)
            )

            st.subheader("Variables categóricas")

            tabla_categoricas = pd.DataFrame({
                "Variable": variables_categoricas,
                "Tipo": "Categórica"
            })

            st.dataframe(
                tabla_categoricas,
                use_container_width=True
            )

            st.metric(
                "Cantidad de variables categóricas",
                len(variables_categoricas)
            )


        # ==========================================
        # ITEM 3
        # ==========================================

        elif item == "Ítem 3: Estadísticas descriptivas":

            st.header("Ítem 3: Estadísticas descriptivas")

            variables_numericas = df.select_dtypes(
                include="number"
            ).columns.tolist()

            if variables_numericas:

                estadisticas = df[
                    variables_numericas
                ].describe().T

                estadisticas["mediana"] = df[
                    variables_numericas
                ].median()

                st.dataframe(
                    estadisticas.round(2),
                    use_container_width=True
                )

                st.write(
                    "La media representa el promedio de los datos. "
                    "La mediana representa el valor central y la "
                    "desviación estándar permite observar la dispersión."
                )

            else:

                st.warning(
                    "No se encontraron variables numéricas."
                )


        # ==========================================
        # ITEM 4
        # ==========================================

        elif item == "Ítem 4: Valores nulos":

            st.header("Ítem 4: Valores nulos")

            nulos = df.isnull().sum()

            tabla_nulos = pd.DataFrame({
                "Variable": df.columns,
                "Valores nulos": nulos.values
            })

            tabla_nulos = tabla_nulos.sort_values(
                "Valores nulos",
                ascending=False
            )

            st.dataframe(
                tabla_nulos,
                use_container_width=True
            )

            total_nulos = int(
                df.isnull().sum().sum()
            )

            st.metric(
                "Total de valores nulos",
                total_nulos
            )

            variables_con_nulos = tabla_nulos[
                tabla_nulos["Valores nulos"] > 0
            ]

            if len(variables_con_nulos) > 0:

                fig, ax = plt.subplots(
                    figsize=(10, 5)
                )

                ax.bar(
                    variables_con_nulos["Variable"].astype(str),
                    variables_con_nulos["Valores nulos"]
                )

                ax.set_title(
                    "Valores nulos por variable"
                )

                ax.set_xlabel("Variable")
                ax.set_ylabel("Valores nulos")

                plt.xticks(rotation=45)

                st.pyplot(fig)

                plt.close(fig)

            else:

                st.success(
                    "El Dataset no contiene valores nulos."
                )


        # ==========================================
        # ITEM 5
        # ==========================================

        elif item == "Ítem 5: Distribución numérica":

            st.header(
                "Ítem 5: Distribución de variables numéricas"
            )

            variables_numericas = df.select_dtypes(
                include="number"
            ).columns.tolist()

            if variables_numericas:

                for variable in variables_numericas:

                    datos = pd.to_numeric(
                        df[variable],
                        errors="coerce"
                    ).dropna()

                    if len(datos) == 0:
                        continue

                    st.subheader(
                        f"Distribución de {variable}"
                    )

                    fig, ax = plt.subplots(
                        figsize=(9, 5)
                    )

                    ax.hist(
                        datos,
                        bins=20
                    )

                    ax.set_title(
                        f"Distribución de {variable}"
                    )

                    ax.set_xlabel(variable)
                    ax.set_ylabel("Frecuencia")

                    st.pyplot(fig)

                    plt.close(fig)

            else:

                st.warning(
                    "No se encontraron variables numéricas."
                )


        # ==========================================
        # ITEM 6
        # ==========================================

        elif item == "Ítem 6: Variables categóricas":

            st.header(
                "Ítem 6: Variables categóricas"
            )

            variables_categoricas = df.select_dtypes(
                include=["object", "category"]
            ).columns.tolist()

            if variables_categoricas:

                for variable in variables_categoricas:

                    st.subheader(
                        f"Variable: {variable}"
                    )

                    conteo = (
                        df[variable]
                        .fillna("Valores nulos")
                        .astype(str)
                        .value_counts()
                    )

                    porcentaje = (
                        conteo /
                        conteo.sum() *
                        100
                    ).round(2)

                    tabla = pd.DataFrame({
                        "Categoría": conteo.index,
                        "Frecuencia": conteo.values,
                        "Porcentaje (%)": porcentaje.values
                    })

                    st.dataframe(
                        tabla,
                        use_container_width=True
                    )

                                        fig, ax = plt.subplots(figsize=(10, 5))

                    ax.bar(
                        conteo.index.astype(str),
                        conteo.values
                    )

                    ax.set_title(f"Distribución de {variable}")
                    ax.set_xlabel(variable)
                    ax.set_ylabel("Frecuencia")

                    plt.setp(
                        ax.get_xticklabels(),
                        rotation=45,
                        ha="right"
                    )

                    fig.tight_layout()

                    st.pyplot(fig, clear_figure=True)

                    plt.close(fig)


        # ==========================================
        # ITEM 7
        # ==========================================

        elif item == "Ítem 7: Numérico vs categórico":

            st.header(
                "Ítem 7: Numérico vs categórico"
            )

            if "Churn" in df.columns:

                variables = []

                for variable in [
                    "MonthlyCharges",
                    "tenure"
                ]:

                    if (
                        variable in df.columns
                        and pd.api.types.is_numeric_dtype(
                            df[variable]
                        )
                    ):

                        variables.append(variable)

                for variable in variables:

                    st.subheader(
                        f"{variable} vs Churn"
                    )

                    fig, ax = plt.subplots(
                        figsize=(8, 5)
                    )

                    sns.boxplot(
                        data=df,
                        x="Churn",
                        y=variable,
                        ax=ax
                    )

                    ax.set_title(
                        f"{variable} según Churn"
                    )

                    st.pyplot(fig)

                    plt.close(fig)

                    resumen = df.groupby(
                        "Churn"
                    )[variable].agg(
                        ["mean", "median", "std"]
                    )

                    st.dataframe(
                        resumen.round(2),
                        use_container_width=True
                    )

            else:

                st.warning(
                    "La variable Churn no se encuentra "
                    "en el Dataset."
                )


        # ==========================================
        # ITEM 8
        # ==========================================

        elif item == "Ítem 8: Categórico vs categórico":

            st.header(
                "Ítem 8: Categórico vs categórico"
            )

            if "Churn" in df.columns:

                variables = []

                for variable in [
                    "Contract",
                    "InternetService"
                ]:

                    if variable in df.columns:

                        variables.append(variable)

                for variable in variables:

                    st.subheader(
                        f"{variable} vs Churn"
                    )

                    tabla = pd.crosstab(
                        df[variable],
                        df["Churn"]
                    )

                    st.dataframe(
                        tabla,
                        use_container_width=True
                    )

                    porcentajes = pd.crosstab(
                        df[variable],
                        df["Churn"],
                        normalize="index"
                    ) * 100

                    st.write(
                        "Porcentajes:"
                    )

                    st.dataframe(
                        porcentajes.round(2),
                        use_container_width=True
                    )

                    fig, ax = plt.subplots(
                        figsize=(9, 5)
                    )

                    tabla.plot(
                        kind="bar",
                        ax=ax
                    )

                    ax.set_title(
                        f"{variable} vs Churn"
                    )

                    ax.set_xlabel(variable)
                    ax.set_ylabel(
                        "Cantidad de clientes"
                    )

                    plt.xticks(
                        rotation=45,
                        ha="right"
                    )

                    st.pyplot(fig)

                    plt.close(fig)

            else:

                st.warning(
                    "La variable Churn no se encuentra "
                    "en el Dataset."
                )


        # ==========================================
        # ITEM 9
        # ==========================================

        elif item == "Ítem 9: Parámetros seleccionados":

            st.header(
                "Ítem 9: Parámetros seleccionados"
            )

            variables_numericas = df.select_dtypes(
                include="number"
            ).columns.tolist()

            variables_categoricas = df.select_dtypes(
                include=["object", "category"]
            ).columns.tolist()

            if variables_numericas:

                variable_numerica = st.selectbox(
                    "Seleccione una variable numérica",
                    variables_numericas
                )

                datos = pd.to_numeric(
                    df[variable_numerica],
                    errors="coerce"
                ).dropna()

                fig, ax = plt.subplots(
                    figsize=(9, 5)
                )

                ax.hist(
                    datos,
                    bins=20
                )

                ax.set_title(
                    f"Distribución de {variable_numerica}"
                )

                ax.set_xlabel(
                    variable_numerica
                )

                ax.set_ylabel(
                    "Frecuencia"
                )

                st.pyplot(fig)

                plt.close(fig)

            if variables_categoricas:

                variables_seleccionadas = st.multiselect(
                    "Seleccione variables categóricas",
                    variables_categoricas
                )

                for variable in variables_seleccionadas:

                    st.subheader(
                        f"Análisis de {variable}"
                    )

                    conteo = (
                        df[variable]
                        .fillna("Valores nulos")
                        .astype(str)
                        .value_counts()
                    )

                    st.dataframe(
                        conteo.to_frame(
                            "Frecuencia"
                        ),
                        use_container_width=True
                    )


        # ==========================================
        # ITEM 10
        # ==========================================

        elif item == "Ítem 10: Hallazgos clave":

            st.header(
                "Ítem 10: Hallazgos clave"
            )

            if "Churn" in df.columns:

                churn_counts = (
                    df["Churn"]
                    .fillna("Valores nulos")
                    .astype(str)
                    .value_counts()
                )

                total_clientes = len(df)

                clientes_churn = churn_counts.get(
                    "Yes",
                    0
                )

                porcentaje_churn = (
                    clientes_churn /
                    total_clientes *
                    100
                    if total_clientes > 0
                    else 0
                )

                col1, col2 = st.columns(2)

                with col1:

                    st.metric(
                        "Clientes analizados",
                        total_clientes
                    )

                with col2:

                    st.metric(
                        "Tasa de Churn",
                        f"{porcentaje_churn:.2f}%"
                    )

                fig, ax = plt.subplots(
                    figsize=(8, 5)
                )

                ax.bar(
                    churn_counts.index.astype(str),
                    churn_counts.values
                )

                ax.set_title(
                    "Distribución de clientes según Churn"
                )

                ax.set_xlabel("Churn")
                ax.set_ylabel(
                    "Cantidad de clientes"
                )

                st.pyplot(fig)

                plt.close(fig)

                st.subheader(
                    "Principales hallazgos"
                )

                if "tenure" in df.columns:

                    promedio_tenure = df.groupby(
                        "Churn"
                    )["tenure"].mean()

                    st.write(
                        "• Se puede comparar la permanencia "
                        "promedio de los clientes según su "
                        "condición de Churn."
                    )

                    st.dataframe(
                        promedio_tenure.round(2).to_frame(
                            "Promedio de tenure"
                        ),
                        use_container_width=True
                    )

                if "MonthlyCharges" in df.columns:

                    promedio_cargos = df.groupby(
                        "Churn"
                    )["MonthlyCharges"].mean()

                    st.write(
                        "• Se puede comparar el cargo mensual "
                        "promedio entre clientes que permanecen "
                        "y clientes que abandonan."
                    )

                    st.dataframe(
                        promedio_cargos.round(2).to_frame(
                            "Promedio MonthlyCharges"
                        ),
                        use_container_width=True
                    )

            else:

                st.warning(
                    "La variable Churn no se encuentra "
                    "en el Dataset."
                )
