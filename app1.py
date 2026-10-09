
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# =========================================================
# CONFIGURACION GENERAL
# =========================================================

st.set_page_config(
    page_title="Telco Customer Churn - EDA",
    page_icon="📊",
    layout="wide"
)

sns.set_theme(style="whitegrid")


# =========================================================
# CLASE: PROGRAMACION ORIENTADA A OBJETOS (POO)
# =========================================================

class DataAnalyzer:

    def __init__(self, dataframe):
        self.df = dataframe.copy()
        self.preparar_datos()

    def preparar_datos(self):
        self.df.columns = self.df.columns.str.strip()

        # Limpiar espacios en variables de texto
        for col in self.df.select_dtypes(include=["object", "string"]).columns:
            self.df[col] = self.df[col].map(
                lambda x: x.strip() if isinstance(x, str) else x
            )

        # Convertir TotalCharges a numerica
        if "TotalCharges" in self.df.columns:
            self.df["TotalCharges"] = pd.to_numeric(
                self.df["TotalCharges"].replace("", np.nan),
                errors="coerce"
            )

        # SeniorCitizen se considera categorica
        if "SeniorCitizen" in self.df.columns:
            self.df["SeniorCitizen"] = self.df["SeniorCitizen"].map(
                lambda x: str(int(x))
                if pd.notna(x) and str(x).replace(".", "", 1).isdigit()
                else x
            )

    def obtener_numericas(self):
        excluir = {
            "CustomerID", "customerID", "customer_id",
            "SeniorCitizen"
        }

        return [
            col for col in self.df.select_dtypes(include=np.number).columns
            if col not in excluir
        ]

    def obtener_categoricas(self):
        numericas = set(self.obtener_numericas())
        identificadores = {
            "CustomerID", "customerID", "customer_id"
        }

        return [
            col for col in self.df.columns
            if col not in numericas and col not in identificadores
        ]

    def clasificar_variables(self):
        filas = []

        for col in self.df.columns:
            if col in {"CustomerID", "customerID", "customer_id"}:
                tipo = "Identificador"
            elif col in self.obtener_numericas():
                tipo = "Numerica"
            else:
                tipo = "Categorica"

            filas.append({
                "Variable": col,
                "Tipo de dato": str(self.df[col].dtype),
                "Clasificacion": tipo,
                "Valores unicos": self.df[col].nunique(),
                "Valores nulos": self.df[col].isna().sum()
            })

        return pd.DataFrame(filas)

    def estadisticas(self):
        numericas = self.obtener_numericas()

        if not numericas:
            return pd.DataFrame()

        resultado = self.df[numericas].describe().T
        resultado["Mediana"] = self.df[numericas].median()
        resultado["Moda"] = self.df[numericas].mode().iloc[0]
        resultado["Nulos"] = self.df[numericas].isna().sum()

        return resultado.reset_index(names="Variable")

    def valores_faltantes(self):
        resultado = pd.DataFrame({
            "Variable": self.df.columns,
            "Valores nulos": self.df.isna().sum().values
        })

        resultado["Porcentaje nulo"] = (
            resultado["Valores nulos"] / len(self.df) * 100
        ).round(2)

        return resultado.sort_values(
            "Valores nulos", ascending=False
        )


# =========================================================
# MODULO 1: HOME
# =========================================================

def mostrar_home():

    st.title("📊 Análisis Exploratorio de Datos")
    st.subheader("Telco Customer Churn")

    st.markdown("""
    ### Objetivo del proyecto

    Realizar un análisis exploratorio de los datos de clientes
    de telecomunicaciones para comprender sus características,
    evaluar la calidad de la información e identificar patrones
    asociados con la deserción de clientes (*Churn*).

    El proyecto tiene un enfoque descriptivo y busca aportar
    información útil para la toma de decisiones. No desarrolla
    modelos predictivos.
    """)

    st.divider()

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 👨‍💻 Autor")
        st.write("**Nombre:** Marlon Jerson Rojas Novoa")
        st.write("**Curso / Especialización:** Data Science")
        st.write("**Año:** 2026")

    with col2:
        st.markdown("### 🗂️ Dataset")
        st.write("""
        El archivo `TelcoCustomerChurn.csv` contiene información
        de clientes, servicios contratados, cargos y permanencia.
        La variable `Churn`, cuando está disponible, identifica
        si el cliente dejó el servicio.
        """)

    st.divider()

    st.markdown("### 🛠️ Tecnologías utilizadas")

    t1, t2, t3, t4 = st.columns(4)
    t1.metric("Lenguaje", "Python")
    t2.metric("Manipulación", "Pandas")
    t3.metric("Visualización", "Matplotlib")
    t4.metric("Aplicación", "Streamlit")

    st.markdown("""
    **Herramientas adicionales:** NumPy, Seaborn y Programación
    Orientada a Objetos (POO).
    """)

    st.info(
        "Para comenzar el análisis, ingresa al módulo "
        "'Carga del dataset' y carga el archivo CSV."
    )


# =========================================================
# MODULO 2: CARGA DEL DATASET
# =========================================================

def cargar_dataset():

    st.header("📂 Módulo 2: Carga del dataset")

    archivo = st.file_uploader(
        "Selecciona el archivo TelcoCustomerChurn.csv",
        type=["csv"],
        help="Carga el archivo CSV antes de ejecutar los análisis."
    )

    if archivo is None:
        st.warning(
            "Debes cargar el archivo CSV para habilitar los "
            "módulos de análisis."
        )
        st.stop()

    try:
        df = pd.read_csv(archivo)

        if df.empty:
            st.error("El archivo CSV no contiene registros.")
            st.stop()

        if len(df.columns) == 0:
            st.error("El archivo no contiene columnas.")
            st.stop()

        st.success("Dataset cargado correctamente.")

        col1, col2 = st.columns(2)

        col1.metric("Cantidad de filas", f"{df.shape[0]:,}")
        col2.metric("Cantidad de columnas", f"{df.shape[1]:,}")

        st.subheader("Vista previa del dataset")
        st.dataframe(df.head(10), use_container_width=True)

        st.caption(
            "Se muestran los primeros 10 registros para verificar "
            "que los datos se hayan cargado correctamente."
        )

        return df

    except Exception as error:
        st.error(f"No fue posible leer el archivo: {error}")
        st.stop()


# =========================================================
# ITEM 1: INFORMACION GENERAL
# =========================================================

def item1(analyzer):

    st.header("Ítem 1. Información general del dataset")

    df = analyzer.df

    st.subheader("Dimensiones")
    st.write(f"Filas: **{df.shape[0]:,}**")
    st.write(f"Columnas: **{df.shape[1]}**")

    st.subheader("Información equivalente a .info()")

    info = pd.DataFrame({
        "Variable": df.columns,
        "Tipo de dato": [str(df[c].dtype) for c in df.columns],
        "Registros no nulos": [df[c].notna().sum() for c in df.columns],
        "Valores nulos": [df[c].isna().sum() for c in df.columns]
    })

    st.dataframe(info, use_container_width=True)

    st.subheader("Tipos de datos")
    st.dataframe(
        df.dtypes.astype(str).rename("Tipo").reset_index(names="Variable"),
        use_container_width=True
    )

    st.write(
        "Esta información permite conocer la estructura del dataset "
        "y detectar variables que requieren conversión o limpieza."
    )


# =========================================================
# ITEM 2: CLASIFICACION DE VARIABLES
# =========================================================

def item2(analyzer):

    st.header("Ítem 2. Clasificación de variables")

    clasificacion = analyzer.clasificar_variables()

    st.dataframe(clasificacion, use_container_width=True)

    numericas = analyzer.obtener_numericas()
    categoricas = analyzer.obtener_categoricas()

    col1, col2, col3 = st.columns(3)

    col1.metric("Variables numéricas", len(numericas))
    col2.metric("Variables categóricas", len(categoricas))

    identificadores = [
        c for c in analyzer.df.columns
        if c.lower() in ["customerid", "customer_id"]
    ]

    col3.metric("Identificadores", len(identificadores))

    st.markdown("#### Variables numéricas")
    st.write(", ".join(numericas) if numericas else "No se encontraron.")

    st.markdown("#### Variables categóricas")
    st.write(", ".join(categoricas) if categoricas else "No se encontraron.")

    st.caption(
        "SeniorCitizen se clasifica como categórica y TotalCharges "
        "como numérica. CustomerID se excluye de los análisis estadísticos."
    )


# =========================================================
# ITEM 3: ESTADISTICAS DESCRIPTIVAS
# =========================================================

def item3(analyzer):

    st.header("Ítem 3. Estadísticas descriptivas")

    estadisticas = analyzer.estadisticas()

    if estadisticas.empty:
        st.warning("No hay variables numéricas disponibles.")
        return

    st.dataframe(
        estadisticas.round(3),
        use_container_width=True
    )

    variable = st.selectbox(
        "Selecciona una variable numérica para interpretarla",
        analyzer.obtener_numericas(),
        key="estadistica_variable"
    )

    datos = analyzer.df[variable].dropna()

    if datos.empty:
        st.warning("La variable no contiene datos válidos.")
        return

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Media", f"{datos.mean():.2f}")
    c2.metric("Mediana", f"{datos.median():.2f}")
    c3.metric("Moda", f"{datos.mode().iloc[0]:.2f}")
    c4.metric("Desviación estándar", f"{datos.std():.2f}")

    if datos.mean() > datos.median():
        st.write(
            "La media supera a la mediana. Esto puede indicar una "
            "distribución con valores altos que elevan el promedio."
        )
    elif datos.mean() < datos.median():
        st.write(
            "La media es inferior a la mediana. Esto puede indicar "
            "una distribución con valores bajos que reducen el promedio."
        )
    else:
        st.write("La media y la mediana tienen valores similares.")

    st.caption(
        "La desviación estándar mide la dispersión respecto de la media. "
        "La interpretación debe contrastarse con la distribución visual."
    )


# =========================================================
# ITEM 4: VALORES FALTANTES
# =========================================================

def item4(analyzer):

    st.header("Ítem 4. Análisis de valores faltantes")

    faltantes = analyzer.valores_faltantes()

    st.dataframe(faltantes, use_container_width=True)

    con_nulos = faltantes[faltantes["Valores nulos"] > 0]

    if con_nulos.empty:
        st.success("No se encontraron valores nulos.")
    else:
        fig, ax = plt.subplots(figsize=(9, 4))

        datos = con_nulos.sort_values("Porcentaje nulo")

        ax.barh(
            datos["Variable"],
            datos["Porcentaje nulo"]
        )

        ax.set_xlabel("Valores faltantes (%)")
        ax.set_title("Porcentaje de valores nulos por variable")

        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

        mayor = con_nulos.sort_values(
            "Porcentaje nulo", ascending=False
        ).iloc[0]

        st.write(
            f"La variable con mayor porcentaje de valores faltantes "
            f"es **{mayor['Variable']}**, con "
            f"**{mayor['Porcentaje nulo']:.2f}%**."
        )

    st.write(
        "Los valores faltantes pueden afectar los resultados. Antes de "
        "eliminarlos o reemplazarlos, debe evaluarse su cantidad y "
        "su posible origen."
    )


# =========================================================
# ITEM 5: DISTRIBUCION NUMERICA
# =========================================================

def item5(analyzer):

    st.header("Ítem 5. Distribución de variables numéricas")

    numericas = analyzer.obtener_numericas()

    if not numericas:
        st.warning("No hay variables numéricas disponibles.")
        return

    seleccion = st.multiselect(
        "Selecciona las variables que deseas visualizar",
        numericas,
        default=numericas[:min(2, len(numericas))]
    )

    intervalos = st.slider(
        "Número de intervalos del histograma",
        min_value=5,
        max_value=60,
        value=25
    )

    if not seleccion:
        st.info("Selecciona al menos una variable.")
        return

    for variable in seleccion:

        datos = analyzer.df[variable].dropna()

        fig, ax = plt.subplots(figsize=(8, 4))

        sns.histplot(
            datos,
            bins=intervalos,
            kde=len(datos) > 1,
            ax=ax
        )

        ax.set_title(f"Distribución de {variable}")
        ax.set_xlabel(variable)
        ax.set_ylabel("Frecuencia")

        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

        if not datos.empty:
            st.write(
                f"**{variable}:** media = {datos.mean():.2f}; "
                f"mediana = {datos.median():.2f}; "
                f"desviación estándar = {datos.std():.2f}."
            )

    st.caption(
        "Los histogramas permiten observar concentración, asimetría "
        "y posibles valores extremos."
    )


# =========================================================
# ITEM 6: VARIABLES CATEGORICAS
# =========================================================

def item6(analyzer):

    st.header("Ítem 6. Análisis de variables categóricas")

    categoricas = analyzer.obtener_categoricas()

    if not categoricas:
        st.warning("No hay variables categóricas disponibles.")
        return

    variable = st.selectbox(
        "Selecciona una variable categórica",
        categoricas,
        key="categoria_item6"
    )

    datos = analyzer.df[variable].fillna("(Nulo)")
    conteo = datos.value_counts()
    porcentaje = datos.value_counts(normalize=True) * 100

    tabla = pd.DataFrame({
        "Categoría": conteo.index.astype(str),
        "Frecuencia": conteo.values,
        "Porcentaje (%)": porcentaje.values.round(2)
    })

    col1, col2 = st.columns([1, 1])

    with col1:
        st.dataframe(tabla, use_container_width=True)

    with col2:
        fig, ax = plt.subplots(figsize=(7, 4))

        tabla_plot = tabla.sort_values("Frecuencia")

        ax.barh(
            tabla_plot["Categoría"],
            tabla_plot["Frecuencia"]
        )

        ax.set_xlabel("Frecuencia")
        ax.set_title(f"Distribución de {variable}")

        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    st.write(
        f"La categoría más frecuente es **{tabla.iloc[0]['Categoría']}**, "
        f"con {tabla.iloc[0]['Frecuencia']} registros "
        f"({tabla.iloc[0]['Porcentaje (%)']:.2f}%)."
    )


# =========================================================
# ITEM 7: NUMERICA VS CHURN
# =========================================================

def item7(analyzer):

    st.header("Ítem 7. Análisis bivariado: numérica vs. Churn")

    df = analyzer.df
    numericas = analyzer.obtener_numericas()

    churn = next(
        (c for c in df.columns if c.lower() == "churn"),
        None
    )

    if churn is None:
        st.warning("No se encontró la variable Churn.")
        return

    if not numericas:
        st.warning("No hay variables numéricas disponibles.")
        return

    preferida = next(
        (c for c in ["MonthlyCharges", "tenure"] if c in numericas),
        numericas[0]
    )

    variable = st.selectbox(
        "Selecciona una variable numérica",
        numericas,
        index=numericas.index(preferida),
        key="numerica_churn"
    )

    datos = df[[variable, churn]].dropna()

    resumen = datos.groupby(churn)[variable].agg(
        ["count", "mean", "median", "std"]
    ).reset_index()

    st.subheader("Comparación estadística por Churn")
    st.dataframe(resumen.round(3), use_container_width=True)

    fig, ax = plt.subplots(figsize=(8, 4))

    sns.boxplot(
        data=datos,
        x=churn,
        y=variable,
        ax=ax
    )

    ax.set_title(f"{variable} según Churn")

    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    st.write(
        "Compara las medianas, la dispersión y los posibles valores "
        "extremos de cada grupo. Una diferencia descriptiva no demuestra "
        "que la variable sea la causa de la deserción."
    )


# =========================================================
# ITEM 8: CATEGORICA VS CHURN
# =========================================================

def item8(analyzer):

    st.header("Ítem 8. Análisis bivariado: categórica vs. Churn")

    df = analyzer.df

    churn = next(
        (c for c in df.columns if c.lower() == "churn"),
        None
    )

    categoricas = [
        c for c in analyzer.obtener_categoricas()
        if c != churn
    ]

    if churn is None:
        st.warning("No se encontró la variable Churn.")
        return

    if not categoricas:
        st.warning("No hay otras variables categóricas disponibles.")
        return

    preferida = next(
        (c for c in ["Contract", "InternetService"] if c in categoricas),
        categoricas[0]
    )

    variable = st.selectbox(
        "Selecciona una variable categórica",
        categoricas,
        index=categoricas.index(preferida),
        key="categorica_churn"
    )

    datos = df[[variable, churn]].copy()
    datos[variable] = datos[variable].fillna("(Nulo)")
    datos[churn] = datos[churn].fillna("(Nulo)")

    conteos = pd.crosstab(datos[variable], datos[churn])
    porcentajes = pd.crosstab(
        datos[variable],
        datos[churn],
        normalize="index"
    ) * 100

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Conteos")
        st.dataframe(conteos, use_container_width=True)

    with col2:
        st.subheader("Porcentajes por categoría")
        st.dataframe(porcentajes.round(2), use_container_width=True)

    fig, ax = plt.subplots(figsize=(9, 5))

    porcentajes.plot(kind="bar", ax=ax)

    ax.set_title(f"Proporción de Churn según {variable}")
    ax.set_xlabel(variable)
    ax.set_ylabel("Porcentaje (%)")
    ax.legend(title=churn)

    plt.xticks(rotation=35, ha="right")
    fig.tight_layout()

    st.pyplot(fig)
    plt.close(fig)

    st.write(
        "La tabla permite comparar cómo se distribuye Churn dentro de "
        "cada categoría. Para tomar decisiones, considera tanto el "
        "porcentaje como la cantidad de clientes de cada grupo."
    )


# =========================================================
# ITEM 9: ANALISIS DINAMICO
# =========================================================

def item9(analyzer):

    st.header("Ítem 9. Análisis dinámico")

    df = analyzer.df.copy()
    numericas = analyzer.obtener_numericas()
    categoricas = analyzer.obtener_categoricas()

    st.write(
        "Selecciona variables y filtros para explorar diferentes "
        "segmentos del dataset."
    )

    filtro = st.selectbox(
        "Variable categórica para filtrar",
        ["Sin filtro"] + categoricas,
        key="filtro_dinamico"
    )

    if filtro != "Sin filtro":

        valores = sorted(
            df[filtro].dropna().astype(str).unique().tolist()
        )

        seleccion = st.multiselect(
            f"Selecciona valores de {filtro}",
            valores,
            default=valores[:min(3, len(valores))],
            key="valores_dinamicos"
        )

        if seleccion:
            df = df[df[filtro].astype(str).isin(seleccion)]
        else:
            df = df.iloc[0:0]

    if numericas and not df.empty:

        variable = st.selectbox(
            "Variable numérica para aplicar un rango",
            numericas,
            key="variable_rango"
        )

        serie = df[variable].dropna()

        if not serie.empty:

            minimo = float(serie.min())
            maximo = float(serie.max())

            if minimo < maximo:

                rango = st.slider(
                    f"Rango de valores de {variable}",
                    min_value=minimo,
                    max_value=maximo,
                    value=(minimo, maximo),
                    key="rango_numerico"
                )

                df = df[
                    df[variable].between(
                        rango[0], rango[1], inclusive="both"
                    )
                ]

    mostrar_tabla = st.checkbox(
        "Mostrar tabla de datos filtrados",
        value=True
    )

    col1, col2 = st.columns(2)

    col1.metric("Registros filtrados", f"{len(df):,}")
    col2.metric("Columnas", len(df.columns))

    if numericas and not df.empty:
        st.subheader("Estadísticas del segmento seleccionado")
        st.dataframe(
            df[numericas].describe().T.round(3),
            use_container_width=True
        )

    if mostrar_tabla:
        st.subheader("Datos filtrados")
        st.dataframe(df.head(500), use_container_width=True)

        if len(df) > 500:
            st.caption("Se muestran como máximo 500 filas en esta vista.")


# =========================================================
# ITEM 10: HALLAZGOS Y CONCLUSIONES
# =========================================================

def item10(analyzer):

    st.header("Ítem 10. Hallazgos clave y conclusiones")

    df = analyzer.df

    churn = next(
        (c for c in df.columns if c.lower() == "churn"),
        None
    )

    st.subheader("Resumen visual")

    if churn is not None:

        conteo = df[churn].fillna("(Nulo)").value_counts()

        fig, ax = plt.subplots(figsize=(7, 4))

        ax.bar(conteo.index.astype(str), conteo.values)

        ax.set_title("Distribución de clientes por Churn")
        ax.set_xlabel("Churn")
        ax.set_ylabel("Cantidad de clientes")

        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

        valores = df[churn].dropna().astype(str).str.strip().str.lower()
        afirmativos = valores.isin(["yes", "si", "sí", "1", "true"])

        if len(valores):
            tasa = afirmativos.mean() * 100
            st.metric("Porcentaje de deserción", f"{tasa:.2f}%")

    else:
        st.warning(
            "No se encontró Churn. Verifica los nombres de las columnas."
        )

    st.subheader("Cinco conclusiones basadas en los datos")

    # Conclusión 1: calidad de datos
    faltantes = analyzer.valores_faltantes()
    con_nulos = faltantes[faltantes["Valores nulos"] > 0]

    if con_nulos.empty:
        conclusion1 = (
            "No se detectaron valores nulos después de la preparación "
            "de los datos."
        )
    else:
        mayor = con_nulos.sort_values(
            "Porcentaje nulo", ascending=False
        ).iloc[0]

        conclusion1 = (
            f"La variable {mayor['Variable']} tiene la mayor proporción "
            f"de valores nulos ({mayor['Porcentaje nulo']:.2f}%). "
            "Se debe revisar antes de realizar análisis adicionales."
        )

    # Conclusión 2: antigüedad
    if "tenure" in df.columns and churn is not None:
        resumen = df.groupby(churn, observed=False)["tenure"].median()

        if len(resumen) >= 2:
            conclusion2 = (
                "La mediana de antigüedad (tenure) por grupo es: "
                + "; ".join(
                    f"{grupo}: {valor:.2f} meses"
                    for grupo, valor in resumen.items()
                )
                + ". Esta diferencia permite investigar el ciclo de vida "
                "del cliente."
            )
        else:
            conclusion2 = (
                "No hay suficientes grupos válidos para comparar "
                "la antigüedad según Churn."
            )
    else:
        conclusion2 = (
            "No se pudo comparar la antigüedad porque falta tenure o Churn."
        )

    # Conclusión 3: cargos mensuales
    if "MonthlyCharges" in df.columns and churn is not None:
        resumen = df.groupby(churn, observed=False)["MonthlyCharges"].median()

        if len(resumen) >= 2:
            conclusion3 = (
                "La mediana de cargos mensuales por grupo es: "
                + "; ".join(
                    f"{grupo}: {valor:.2f}"
                    for grupo, valor in resumen.items()
                )
                + ". Conviene contrastar este resultado con los servicios "
                "y contratos de cada segmento."
            )
        else:
            conclusion3 = (
                "No hay suficientes grupos para comparar cargos mensuales."
            )
    else:
        conclusion3 = (
            "No se pudo comparar MonthlyCharges porque falta esa variable "
            "o Churn."
        )

    # Conclusión 4: contrato
    if "Contract" in df.columns and churn is not None:
        temporal = df[["Contract", churn]].dropna().copy()
        temporal[churn] = (
            temporal[churn].astype(str).str.strip().str.lower()
        )

        afirmativo = temporal[churn].isin(["yes", "si", "sí", "1", "true"])
        tasas = afirmativo.groupby(temporal["Contract"]).mean() * 100

        if not tasas.empty:
            grupo_mayor = tasas.idxmax()
            grupo_menor = tasas.idxmin()

            conclusion4 = (
                f"La proporción de deserción más alta por contrato se "
                f"observa en {grupo_mayor} ({tasas[grupo_mayor]:.2f}%) "
                f"y la más baja en {grupo_menor} "
                f"({tasas[grupo_menor]:.2f}%). Considera también el "
                "tamaño de cada grupo antes de priorizar acciones."
            )
        else:
            conclusion4 = (
                "No fue posible comparar la deserción por tipo de contrato."
            )
    else:
        conclusion4 = (
            "No se pudo evaluar el contrato porque falta Contract o Churn."
        )

    # Conclusión 5: servicio de internet
    if "InternetService" in df.columns and churn is not None:
        temporal = df[["InternetService", churn]].dropna().copy()
        temporal[churn] = (
            temporal[churn].astype(str).str.strip().str.lower()
        )

        afirmativo = temporal[churn].isin(["yes", "si", "sí", "1", "true"])
        tasas = afirmativo.groupby(temporal["InternetService"]).mean() * 100

        if not tasas.empty:
            grupo_mayor = tasas.idxmax()
            grupo_menor = tasas.idxmin()

            conclusion5 = (
                f"La mayor proporción de deserción por servicio de internet "
                f"corresponde a {grupo_mayor} ({tasas[grupo_mayor]:.2f}%) "
                f"y la menor a {grupo_menor} "
                f"({tasas[grupo_menor]:.2f}%). Este hallazgo puede orientar "
                "una revisión de la experiencia por tipo de servicio."
            )
        else:
            conclusion5 = (
                "No fue posible comparar la deserción por servicio de internet."
            )
    else:
        conclusion5 = (
            "No se pudo comparar InternetService porque falta esa variable "
            "o Churn."
        )

    conclusiones = [
        conclusion1,
        conclusion2,
        conclusion3,
        conclusion4,
        conclusion5
    ]

    for i, conclusion in enumerate(conclusiones, start=1):
        st.markdown(f"**Conclusión {i}.** {conclusion}")

    st.info(
        "Las conclusiones describen patrones del dataset. No demuestran "
        "causalidad ni predicen el comportamiento futuro de los clientes."
    )


# =========================================================
# APLICACION PRINCIPAL
# =========================================================

def main():

    st.sidebar.title("Menú principal")

    modulo = st.sidebar.radio(
        "Selecciona un módulo",
        [
            "Módulo 1: Home",
            "Módulo 2: Carga del dataset",
            "Ítem 1: Información general",
            "Ítem 2: Clasificación de variables",
            "Ítem 3: Estadísticas descriptivas",
            "Ítem 4: Valores faltantes",
            "Ítem 5: Distribución numérica",
            "Ítem 6: Variables categóricas",
            "Ítem 7: Numérica vs. Churn",
            "Ítem 8: Categórica vs. Churn",
            "Ítem 9: Análisis dinámico",
            "Ítem 10: Hallazgos y conclusiones"
        ]
    )

    # Home es informativo y no carga ni analiza el dataset.
    if modulo == "Módulo 1: Home":
        mostrar_home()
        st.stop()

    # Todos los demás módulos requieren cargar el CSV.
    df = cargar_dataset()

    analyzer = DataAnalyzer(df)

    if modulo == "Módulo 2: Carga del dataset":
        st.success(
            "Carga validada. El dataset está listo para los módulos de análisis."
        )

    elif modulo == "Ítem 1: Información general":
        item1(analyzer)

    elif modulo == "Ítem 2: Clasificación de variables":
        item2(analyzer)

    elif modulo == "Ítem 3: Estadísticas descriptivas":
        item3(analyzer)

    elif modulo == "Ítem 4: Valores faltantes":
        item4(analyzer)

    elif modulo == "Ítem 5: Distribución numérica":
        item5(analyzer)

    elif modulo == "Ítem 6: Variables categóricas":
        item6(analyzer)

    elif modulo == "Ítem 7: Numérica vs. Churn":
        item7(analyzer)

    elif modulo == "Ítem 8: Categórica vs. Churn":
        item8(analyzer)

    elif modulo == "Ítem 9: Análisis dinámico":
        item9(analyzer)

    elif modulo == "Ítem 10: Hallazgos y conclusiones":
        item10(analyzer)


if __name__ == "__main__":
    main()
