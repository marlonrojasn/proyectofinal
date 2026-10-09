
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# --------------------------------------------------
# CONFIGURACIÓN GENERAL
# --------------------------------------------------

st.set_page_config(
    page_title="Proyecto Análisis Churn",
    layout="wide"
)

st.title("Proyecto Análisis Churn")

try:
    st.image("imagen1.jpg")
except Exception:
    pass

try:
    st.sidebar.image("internet.jpg", width=150)
except Exception:
    pass

sns.set_theme(style="whitegrid")


# --------------------------------------------------
# CLASE PARA EL ANÁLISIS DE DATOS
# --------------------------------------------------

class DataAnalyzer:

    def __init__(self, dataframe):
        self.df = dataframe.copy()
        self.df.columns = self.df.columns.str.strip()

        # Convertir TotalCharges a numérica cuando exista.
        if "TotalCharges" in self.df.columns:
            self.df["TotalCharges"] = pd.to_numeric(
                self.df["TotalCharges"],
                errors="coerce"
            )

        # SeniorCitizen representa categorías: 0 y 1.
        if "SeniorCitizen" in self.df.columns:
            self.df["SeniorCitizen"] = (
                self.df["SeniorCitizen"]
                .map({0: "No", 1: "Sí", "0": "No", "1": "Sí"})
                .fillna(self.df["SeniorCitizen"].astype(str))
            )

    def obtener_numericas(self):
        columnas = self.df.select_dtypes(
            include=["number"]
        ).columns.tolist()

        identificadores = [
            col for col in columnas
            if col.lower() in [
                "customerid", "customer_id", "id"
            ]
        ]

        return [
            col for col in columnas
            if col not in identificadores
        ]

    def obtener_categoricas(self):
        numericas = self.obtener_numericas()

        return [
            col for col in self.df.columns
            if col not in numericas
            and col.lower() not in [
                "customerid", "customer_id", "id"
            ]
        ]

    def clasificar_variables(self):
        filas = []

        for columna in self.df.columns:
            valores_unicos = self.df[columna].nunique(
                dropna=True
            )

            if columna.lower() in [
                "customerid", "customer_id", "id"
            ]:
                tipo = "Identificador"
            elif columna == "SeniorCitizen":
                tipo = "Categórica"
            elif pd.api.types.is_numeric_dtype(
                self.df[columna]
            ):
                tipo = "Numérica"
            else:
                tipo = "Categórica"

            filas.append({
                "Variable": columna,
                "Tipo de variable": tipo,
                "Valores únicos": valores_unicos,
                "Valores faltantes": self.df[columna].isna().sum()
            })

        return pd.DataFrame(filas)

    def resumen_numerico(self):
        columnas = self.obtener_numericas()

        if not columnas:
            return pd.DataFrame()

        return self.df[columnas].describe().T

    def resumen_faltantes(self):
        resultado = pd.DataFrame({
            "Variable": self.df.columns,
            "Valores faltantes": self.df.isna().sum().values,
            "Porcentaje (%)": (
                self.df.isna().mean().values * 100
            ).round(2)
        })

        return resultado.sort_values(
            "Valores faltantes",
            ascending=False
        )


# --------------------------------------------------
# FUNCIONES AUXILIARES
# --------------------------------------------------

def buscar_columna(df, nombre):
    """Busca una columna ignorando mayúsculas y minúsculas."""

    for columna in df.columns:
        if columna.lower() == nombre.lower():
            return columna

    return None


def mostrar_grafico(figura):
    st.pyplot(figura)
    plt.close(figura)


def cargar_dataset():
    st.subheader("Carga del dataset")

    archivo = st.file_uploader(
        "Selecciona el archivo TelcoCustomerChurn.csv",
        type=["csv"],
        key="archivo_csv"
    )

    if archivo is None:
        st.info(
            "Carga el archivo CSV para habilitar los módulos "
            "de análisis. Puedes regresar a Home sin cargar datos."
        )
        st.stop()

    try:
        df = pd.read_csv(archivo)
    except Exception as error:
        st.error(f"No se pudo leer el archivo CSV: {error}")
        st.stop()

    if df.empty:
        st.error("El archivo no contiene registros.")
        st.stop()

    df.columns = df.columns.str.strip()

    st.success("Dataset cargado correctamente.")

    tab1, tab2, tab3 = st.tabs([
        "Vista previa",
        "Dimensiones",
        "Tipos de datos"
    ])

    with tab1:
        st.write("Primeras 10 filas:")
        st.dataframe(df.head(10), use_container_width=True)

    with tab2:
        col1, col2 = st.columns(2)

        with col1:
            st.metric("Registros", f"{df.shape[0]:,}")

        with col2:
            st.metric("Columnas", df.shape[1])

    with tab3:
        tipos = pd.DataFrame({
            "Variable": df.columns,
            "Tipo de dato": [
                str(tipo) for tipo in df.dtypes
            ]
        })

        st.dataframe(tipos, use_container_width=True)

    return df


# --------------------------------------------------
# MÓDULO 1: HOME
# --------------------------------------------------

def mostrar_home():

    st.header("Presentación del proyecto")

    st.write(
        "Este proyecto desarrolla un análisis exploratorio "
        "de los datos de clientes de una empresa de "
        "telecomunicaciones. El objetivo es conocer las "
        "características de los clientes y revisar qué "
        "comportamientos aparecen asociados a la deserción "
        "del servicio, identificada mediante la variable Churn."
    )

    st.subheader("Datos del autor")

    col1, col2 = st.columns(2)

    with col1:
        st.write("**Nombre:** Marlon Jerson Rojas Novoa")
        st.write("**Especialización:** Data Science")
        st.write("**Año:** 2026")

    with col2:
        st.write("**Dataset:** TelcoCustomerChurn.csv")
        st.write("**Tipo de trabajo:** Análisis exploratorio de datos")

    st.divider()

    st.subheader("Descripción del dataset")

    st.write(
        "El archivo contiene información sobre los clientes, "
        "los servicios contratados, la antigüedad, los cargos "
        "mensuales y otras características de la relación con "
        "la empresa. La variable Churn permite diferenciar a "
        "los clientes que dejaron el servicio de quienes "
        "continúan, siempre que dicha variable esté presente."
    )

    st.subheader("Herramientas utilizadas")

    st.write(
        "- Python para desarrollar la aplicación.\n"
        "- Pandas y NumPy para preparar y analizar los datos.\n"
        "- Matplotlib y Seaborn para elaborar gráficos.\n"
        "- Streamlit para crear la interfaz interactiva."
    )

    st.subheader("Alcance del análisis")

    st.write(
        "Se revisará la estructura del archivo, la clasificación "
        "de las variables, las estadísticas descriptivas, los "
        "valores faltantes, las distribuciones y las relaciones "
        "entre variables. Las conclusiones serán descriptivas "
        "y estarán basadas en los datos disponibles."
    )

    st.info(
        "Para comenzar, selecciona un módulo en el menú lateral "
        "y carga el archivo CSV cuando se solicite."
    )


# --------------------------------------------------
# MÓDULO 3: PUNTO 1 - INFORMACIÓN GENERAL
# --------------------------------------------------

def item1(df):

    st.header("Punto 1. Información general del dataset")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric("Registros", f"{df.shape[0]:,}")

    with col2:
        st.metric("Variables", df.shape[1])

    with col3:
        st.metric(
            "Celdas vacías",
            f"{int(df.isna().sum().sum()):,}"
        )

    st.subheader("Estructura de los datos")

    informacion = pd.DataFrame({
        "Variable": df.columns,
        "Tipo de dato": [
            str(tipo) for tipo in df.dtypes
        ],
        "Valores no nulos": df.notna().sum().values,
        "Valores faltantes": df.isna().sum().values
    })

    st.dataframe(informacion, use_container_width=True)

    st.subheader("Resumen de la estructura")

    st.write(
        f"El dataset contiene {df.shape[0]:,} registros "
        f"y {df.shape[1]} variables. "
        f"Se identificaron {int(df.isna().sum().sum()):,} "
        "valores faltantes en total."
    )

    st.caption(
        "Los tipos de datos se revisarán con mayor detalle "
        "en el punto de clasificación de variables."
    )


# --------------------------------------------------
# PUNTO 2 - CLASIFICACIÓN DE VARIABLES
# --------------------------------------------------

def item2(df, analyzer):

    st.header("Punto 2. Clasificación de variables")

    clasificacion = analyzer.clasificar_variables()

    st.dataframe(
        clasificacion,
        use_container_width=True
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Variables numéricas",
            int((clasificacion["Tipo de variable"] == "Numérica").sum())
        )

    with col2:
        st.metric(
            "Variables categóricas",
            int((clasificacion["Tipo de variable"] == "Categórica").sum())
        )

    with col3:
        st.metric(
            "Identificadores",
            int((clasificacion["Tipo de variable"] == "Identificador").sum())
        )

    st.subheader("Criterio de clasificación")

    st.write(
        "Las variables numéricas representan cantidades que "
        "pueden resumirse mediante medidas estadísticas. Las "
        "categóricas identifican grupos o atributos, aunque "
        "algunas estén codificadas con números."
    )

    st.write(
        "**SeniorCitizen:** se considera categórica porque "
        "sus valores 0 y 1 representan dos grupos de clientes, "
        "no una cantidad para realizar operaciones estadísticas."
    )

    if "TotalCharges" in df.columns:
        st.write(
            "**TotalCharges:** se considera numérica, ya que "
            "representa el total facturado al cliente. Los "
            "valores vacíos o no convertibles se tratan como "
            "faltantes."
        )

    identificadores = [
        col for col in df.columns
        if col.lower() in [
            "customerid", "customer_id", "id"
        ]
    ]

    if identificadores:
        st.write(
            "**Identificadores:** "
            + ", ".join(identificadores)
            + " se identifican como códigos de cliente. "
            "No se consideran variables explicativas del "
            "comportamiento porque funcionan como identificadores."
        )


# --------------------------------------------------
# PUNTO 3 - ESTADÍSTICA DESCRIPTIVA
# --------------------------------------------------

def item3(df, analyzer):

    st.header("Punto 3. Estadística descriptiva")

    numericas = analyzer.obtener_numericas()

    if not numericas:
        st.warning("No se encontraron variables numéricas.")
        return

    resumen = analyzer.resumen_numerico()

    st.subheader("Resumen estadístico")

    st.dataframe(
        resumen.round(2),
        use_container_width=True
    )

    st.subheader("Medidas centrales y dispersión")

    variable = st.selectbox(
        "Selecciona una variable numérica",
        numericas,
        key="estadistica_variable"
    )

    datos = df[variable].dropna()

    if datos.empty:
        st.warning("La variable seleccionada no tiene datos válidos.")
        return

    moda = datos.mode()

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric("Media", f"{datos.mean():.2f}")

    with col2:
        st.metric("Mediana", f"{datos.median():.2f}")

    with col3:
        st.metric("Desviación estándar", f"{datos.std():.2f}")

    with col4:
        valor_moda = (
            str(round(float(moda.iloc[0]), 2))
            if not moda.empty else "No disponible"
        )
        st.metric("Moda", valor_moda)

    st.write(
        f"Para **{variable}**, la media es {datos.mean():.2f} "
        f"y la mediana es {datos.median():.2f}. "
        "La diferencia entre ambas puede dar una referencia "
        "sobre la simetría de la distribución. La desviación "
        "estándar permite observar cuánto varían los valores "
        "respecto de su media."
    )


# --------------------------------------------------
# PUNTO 4 - VALORES FALTANTES
# --------------------------------------------------

def item4(df, analyzer):

    st.header("Punto 4. Análisis de valores faltantes")

    faltantes = analyzer.resumen_faltantes()

    st.dataframe(
        faltantes,
        use_container_width=True
    )

    total_faltantes = int(df.isna().sum().sum())

    if total_faltantes == 0:
        st.success(
            "No se encontraron valores faltantes representados "
            "como nulos en el dataset."
        )
    else:
        st.warning(
            f"Se encontraron {total_faltantes:,} valores faltantes. "
            "Antes de eliminarlos o reemplazarlos, conviene revisar "
            "en qué variables aparecen y qué significan."
        )

        con_faltantes = faltantes[
            faltantes["Valores faltantes"] > 0
        ].sort_values("Valores faltantes")

        figura, ax = plt.subplots(figsize=(9, 5))

        ax.barh(
            con_faltantes["Variable"],
            con_faltantes["Valores faltantes"]
        )

        ax.set_title("Valores faltantes por variable")
        ax.set_xlabel("Cantidad de valores faltantes")
        ax.set_ylabel("Variable")
        figura.tight_layout()

        mostrar_grafico(figura)

    st.caption(
        "Los espacios en blanco que no se hayan convertido "
        "a valores nulos pueden requerir una revisión adicional."
    )


# --------------------------------------------------
# PUNTO 5 - DISTRIBUCIONES NUMÉRICAS
# --------------------------------------------------

def item5(df, analyzer):

    st.header("Punto 5. Distribución de variables numéricas")

    numericas = analyzer.obtener_numericas()

    if not numericas:
        st.warning("No hay variables numéricas para visualizar.")
        return

    variables = st.multiselect(
        "Selecciona las variables que deseas analizar",
        numericas,
        default=numericas[:min(3, len(numericas))],
        key="hist_variables"
    )

    if not variables:
        st.info("Selecciona al menos una variable.")
        return

    columnas = st.columns(min(2, len(variables)))

    for i, variable in enumerate(variables):
        datos = df[variable].dropna()

        with columnas[i % len(columnas)]:
            figura, ax = plt.subplots(figsize=(7, 4))

            ax.hist(
                datos,
                bins=25,
                edgecolor="black"
            )

            ax.set_title(f"Distribución de {variable}")
            ax.set_xlabel(variable)
            ax.set_ylabel("Frecuencia")

            figura.tight_layout()
            mostrar_grafico(figura)

            if not datos.empty:
                st.write(
                    f"**{variable}:** media = {datos.mean():.2f}; "
                    f"mediana = {datos.median():.2f}; "
                    f"mínimo = {datos.min():.2f}; "
                    f"máximo = {datos.max():.2f}."
                )


# --------------------------------------------------
# PUNTO 6 - DISTRIBUCIÓN CATEGÓRICA
# --------------------------------------------------

def item6(df, analyzer):

    st.header("Punto 6. Distribución de variables categóricas")

    categoricas = analyzer.obtener_categoricas()

    if not categoricas:
        st.warning("No hay variables categóricas disponibles.")
        return

    variable = st.selectbox(
        "Selecciona una variable categórica",
        categoricas,
        key="categoria_variable"
    )

    incluir_nulos = st.checkbox(
        "Mostrar los valores faltantes como una categoría",
        value=True,
        key="categorias_nulos"
    )

    if incluir_nulos:
        frecuencias = (
            df[variable]
            .fillna("Valor faltante")
            .astype(str)
            .value_counts()
        )
    else:
        frecuencias = (
            df[variable]
            .dropna()
            .astype(str)
            .value_counts()
        )

    if frecuencias.empty:
        st.warning("No hay valores para mostrar.")
        return

    tabla = pd.DataFrame({
        "Categoría": frecuencias.index,
        "Frecuencia": frecuencias.values,
        "Porcentaje (%)": (
            frecuencias.values / frecuencias.sum() * 100
        ).round(2)
    })

    col1, col2 = st.columns([1, 1])

    with col1:
        st.dataframe(tabla, use_container_width=True)

    with col2:
        figura, ax = plt.subplots(figsize=(7, 5))

        frecuencias.sort_values().plot(
            kind="barh",
            ax=ax
        )

        ax.set_title(f"Frecuencia de {variable}")
        ax.set_xlabel("Número de clientes")
        ax.set_ylabel(variable)

        figura.tight_layout()
        mostrar_grafico(figura)

    categoria_principal = str(frecuencias.index[0])
    proporcion = frecuencias.iloc[0] / frecuencias.sum() * 100

    st.write(
        f"La categoría con mayor frecuencia es "
        f"**{categoria_principal}**, que representa "
        f"el {proporcion:.2f}% de los registros considerados."
    )


# --------------------------------------------------
# PUNTO 7 - NUMÉRICA FRENTE A CHURN
# --------------------------------------------------

def item7(df):

    st.header("Punto 7. Variables numéricas frente a Churn")

    churn_col = buscar_columna(df, "Churn")

    if churn_col is None:
        st.warning(
            "No se encontró la variable Churn en el archivo."
        )
        return

    variables_objetivo = ["MonthlyCharges", "tenure"]
    disponibles = [
        buscar_columna(df, variable)
        for variable in variables_objetivo
    ]
    disponibles = [
        variable for variable in disponibles
        if variable is not None
        and pd.api.types.is_numeric_dtype(df[variable])
    ]

    if not disponibles:
        st.warning(
            "No se encontraron las variables MonthlyCharges "
            "o tenure como variables numéricas."
        )
        return

    for variable in disponibles:
        figura, ax = plt.subplots(figsize=(8, 4))

        sns.boxplot(
            data=df,
            x=churn_col,
            y=variable,
            ax=ax
        )

        ax.set_title(f"{variable} según {churn_col}")
        ax.set_xlabel("Churn")
        ax.set_ylabel(variable)

        figura.tight_layout()
        mostrar_grafico(figura)

        resumen = (
            df.groupby(churn_col, observed=False)[variable]
            .agg(["count", "mean", "median"])
            .round(2)
        )

        st.write(f"**Resumen de {variable} por Churn**")
        st.dataframe(resumen, use_container_width=True)

        if len(resumen) >= 2:
            st.write(
                "Compara las medianas y la dispersión entre los "
                "grupos. Las diferencias describen el dataset, "
                "pero por sí solas no demuestran que una variable "
                "cause la deserción."
            )


# --------------------------------------------------
# PUNTO 8 - CATEGÓRICA FRENTE A CATEGÓRICA
# --------------------------------------------------

def item8(df):

    st.header("Punto 8. Relación entre variables categóricas")

    churn_col = buscar_columna(df, "Churn")

    if churn_col is None:
        st.warning(
            "No se encontró la variable Churn en el archivo."
        )
        return

    variables_objetivo = ["Contract", "InternetService"]

    disponibles = [
        buscar_columna(df, variable)
        for variable in variables_objetivo
    ]

    disponibles = [
        variable for variable in disponibles
        if variable is not None and variable != churn_col
    ]

    if not disponibles:
        st.warning(
            "No se encontraron Contract o InternetService "
            "en el archivo."
        )
        return

    for variable in disponibles:
        st.subheader(f"{variable} frente a {churn_col}")

        tabla = pd.crosstab(
            df[variable].fillna("Valor faltante"),
            df[churn_col].fillna("Valor faltante")
        )

        st.write("Cantidad de clientes:")
        st.dataframe(tabla, use_container_width=True)

        porcentajes = pd.crosstab(
            df[variable].fillna("Valor faltante"),
            df[churn_col].fillna("Valor faltante"),
            normalize="index"
        ) * 100

        st.write("Porcentaje dentro de cada categoría:")
        st.dataframe(
            porcentajes.round(2),
            use_container_width=True
        )

        figura, ax = plt.subplots(figsize=(8, 4))

        porcentajes.plot(
            kind="bar",
            stacked=True,
            ax=ax
        )

        ax.set_title(f"Distribución porcentual de {churn_col} por {variable}")
        ax.set_xlabel(variable)
        ax.set_ylabel("Porcentaje (%)")
        ax.legend(title=churn_col, bbox_to_anchor=(1.02, 1))

        figura.tight_layout()
        mostrar_grafico(figura)

        st.write(
            "La tabla permite comparar la proporción de clientes "
            "con y sin deserción dentro de cada categoría. Conviene "
            "considerar también el tamaño de cada grupo antes de "
            "interpretar las diferencias."
        )


# --------------------------------------------------
# PUNTO 9 - ANÁLISIS DINÁMICO
# --------------------------------------------------

def item9(df, analyzer):

    st.header("Punto 9. Análisis dinámico")

    st.write(
        "Selecciona las variables que deseas revisar y "
        "ajusta los parámetros para explorar los datos."
    )

    columnas = df.columns.tolist()

    variable = st.selectbox(
        "Variable principal",
        columnas,
        key="dinamica_variable"
    )

    variables_comparacion = st.multiselect(
        "Otras variables para consultar",
        [col for col in columnas if col != variable],
        key="dinamica_comparacion"
    )

    cantidad = st.slider(
        "Cantidad de categorías o valores que se mostrarán",
        min_value=3,
        max_value=20,
        value=10,
        key="dinamica_cantidad"
    )

    mostrar_tabla = st.checkbox(
        "Mostrar tabla de datos",
        value=True,
        key="dinamica_tabla"
    )

    if pd.api.types.is_numeric_dtype(df[variable]):
        st.subheader(f"Resumen de {variable}")

        datos = df[variable].dropna()

        if not datos.empty:
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric("Media", f"{datos.mean():.2f}")

            with col2:
                st.metric("Mediana", f"{datos.median():.2f}")

            with col3:
                st.metric("Desviación estándar", f"{datos.std():.2f}")

            figura, ax = plt.subplots(figsize=(8, 4))
            ax.hist(datos, bins=cantidad, edgecolor="black")
            ax.set_title(f"Distribución de {variable}")
            ax.set_xlabel(variable)
            ax.set_ylabel("Frecuencia")
            figura.tight_layout()
            mostrar_grafico(figura)

    else:
        frecuencias = (
            df[variable]
            .fillna("Valor faltante")
            .astype(str)
            .value_counts()
            .head(cantidad)
        )

        st.subheader(f"Frecuencia de {variable}")

        if not frecuencias.empty:
            figura, ax = plt.subplots(figsize=(8, 4))
            frecuencias.sort_values().plot(
                kind="barh",
                ax=ax
            )
            ax.set_xlabel("Frecuencia")
            ax.set_ylabel(variable)
            figura.tight_layout()
            mostrar_grafico(figura)

    if variables_comparacion:
        st.subheader("Vista de las variables seleccionadas")

        columnas_mostrar = [variable] + variables_comparacion

        if mostrar_tabla:
            st.dataframe(
                df[columnas_mostrar].head(cantidad),
                use_container_width=True
            )

        variable_comparar = st.selectbox(
            "Variable para cruzar con la principal",
            variables_comparacion,
            key="dinamica_cruce"
        )

        tabla_cruce = pd.crosstab(
            df[variable].fillna("Valor faltante").astype(str),
            df[variable_comparar].fillna("Valor faltante").astype(str)
        )

        st.write("Tabla de frecuencias cruzadas:")
        st.dataframe(
            tabla_cruce,
            use_container_width=True
        )

    elif mostrar_tabla:
        st.dataframe(
            df[[variable]].head(cantidad),
            use_container_width=True
        )


# --------------------------------------------------
# PUNTO 10 - HALLAZGOS Y CONCLUSIONES
# --------------------------------------------------

def item10(df):

    st.header("Punto 10. Hallazgos y conclusiones")

    churn_col = buscar_columna(df, "Churn")

    if churn_col is None:
        st.warning(
            "No se encontró Churn. Revisa si la columna existe "
            "en el archivo cargado."
        )
        st.write(
            "Se puede continuar con conclusiones sobre la "
            "estructura y calidad general de los datos."
        )
        return

    total = len(df)
    churn = df[churn_col].astype(str).str.strip()

    churn_si = churn.str.lower().isin(["yes", "sí", "si", "true", "1"])
    churn_no = churn.str.lower().isin(["no", "false", "0"])

    validos = churn_si | churn_no
    total_validos = int(validos.sum())

    if total_validos > 0:
        porcentaje_churn = churn_si.sum() / total_validos * 100
        st.metric(
            "Porcentaje de deserción en registros válidos",
            f"{porcentaje_churn:.2f}%"
        )
    else:
        porcentaje_churn = None
        st.warning(
            "No fue posible interpretar los valores de Churn "
            "como categorías afirmativas y negativas habituales."
        )

    st.subheader("Resumen visual de Churn")

    conteos = churn.value_counts(dropna=False)

    figura, ax = plt.subplots(figsize=(7, 4))
    conteos.plot(kind="bar", ax=ax)
    ax.set_title("Cantidad de registros por categoría de Churn")
    ax.set_xlabel("Churn")
    ax.set_ylabel("Cantidad de registros")
    figura.tight_layout()
    mostrar_grafico(figura)

    st.subheader("Conclusiones basadas en los datos")

    st.write(
        f"**1. Tamaño del dataset.** El archivo contiene "
        f"{total:,} registros y {df.shape[1]} variables, "
        "lo que permite estudiar distintas características "
        "de los clientes."
    )

    faltantes = int(df.isna().sum().sum())

    st.write(
        f"**2. Calidad de los datos.** Se encontraron "
        f"{faltantes:,} valores faltantes representados como nulos. "
        "Estos deben considerarse al interpretar los resultados."
    )

    tenure_col = buscar_columna(df, "tenure")

    if tenure_col is not None:
        datos_tenure = df[[tenure_col]].copy()
        datos_tenure["_grupo_churn"] = churn

        resumen_tenure = datos_tenure.groupby(
            "_grupo_churn"
        )[tenure_col].median()

        if not resumen_tenure.empty:
            detalle = ", ".join(
                f"{grupo}: {valor:.1f}"
                for grupo, valor in resumen_tenure.items()
                if pd.notna(valor)
            )

            st.write(
                "**3. Antigüedad del cliente.** La mediana de "
                f"tenure por grupo de Churn es: {detalle}. "
                "La comparación ayuda a observar diferencias "
                "en la antigüedad de los clientes."
            )
    else:
        st.write(
            "**3. Antigüedad del cliente.** No se encontró "
            "la variable tenure para realizar esta comparación."
        )

    monthly_col = buscar_columna(df, "MonthlyCharges")

    if monthly_col is not None:
        resumen_cargos = df.assign(
            _grupo_churn=churn
        ).groupby("_grupo_churn")[monthly_col].mean()

        detalle_cargos = ", ".join(
            f"{grupo}: {valor:.2f}"
            for grupo, valor in resumen_cargos.items()
            if pd.notna(valor)
        )

        st.write(
            "**4. Cargos mensuales.** El promedio de "
            f"MonthlyCharges por grupo de Churn es: {detalle_cargos}. "
            "Esta comparación describe diferencias de facturación "
            "entre los grupos."
        )
    else:
        st.write(
            "**4. Cargos mensuales.** No se encontró "
            "MonthlyCharges en el dataset."
        )

    contract_col = buscar_columna(df, "Contract")

    if contract_col is not None:
        tabla = pd.crosstab(
            df[contract_col],
            churn,
            normalize="index"
        ) * 100

        st.write(
            "**5. Tipo de contrato.** La distribución porcentual "
            "de Churn por tipo de contrato permite identificar "
            "si los grupos presentan proporciones diferentes."
        )

        st.dataframe(
            tabla.round(2),
            use_container_width=True
        )
    else:
        st.write(
            "**5. Tipo de contrato.** No se encontró la variable "
            "Contract para completar esta comparación."
        )

    st.info(
        "Estas conclusiones describen asociaciones observadas "
        "en el dataset. No deben interpretarse como prueba de "
        "causalidad ni como predicciones sobre clientes futuros."
    )


# --------------------------------------------------
# NAVEGACIÓN PRINCIPAL
# --------------------------------------------------

def main():

    st.sidebar.title("Menú principal")

    modulo = st.sidebar.radio(
        "Selecciona un módulo",
        [
            "Módulo 1: Home",
            "Módulo 2: Carga del dataset",
            "Punto 1: Información general",
            "Punto 2: Clasificación de variables",
            "Punto 3: Estadística descriptiva",
            "Punto 4: Valores faltantes",
            "Punto 5: Distribuciones numéricas",
            "Punto 6: Variables categóricas",
            "Punto 7: Numérica vs Churn",
            "Punto 8: Categórica vs categórica",
            "Punto 9: Análisis dinámico",
            "Punto 10: Hallazgos y conclusiones"
        ]
    )

    if modulo == "Módulo 1: Home":
        mostrar_home()
        st.stop()

    df = cargar_dataset()
    analyzer = DataAnalyzer(df)

    if modulo == "Módulo 2: Carga del dataset":
        st.header("Módulo 2. Carga del dataset")
        st.write(
            "El archivo se ha cargado correctamente. "
            "En las pestañas superiores puedes consultar la "
            "vista previa, las dimensiones y los tipos de datos."
        )

    elif modulo == "Punto 1: Información general":
        item1(df)

    elif modulo == "Punto 2: Clasificación de variables":
        item2(df, analyzer)

    elif modulo == "Punto 3: Estadística descriptiva":
        item3(df, analyzer)

    elif modulo == "Punto 4: Valores faltantes":
        item4(df, analyzer)

    elif modulo == "Punto 5: Distribuciones numéricas":
        item5(df, analyzer)

    elif modulo == "Punto 6: Variables categóricas":
        item6(df, analyzer)

    elif modulo == "Punto 7: Numérica vs Churn":
        item7(df)

    elif modulo == "Punto 8: Categórica vs categórica":
        item8(df)

    elif modulo == "Punto 9: Análisis dinámico":
        item9(df, analyzer)

    elif modulo == "Punto 10: Hallazgos y conclusiones":
        item10(df)


if __name__ == "__main__":
    main()
