
import streamlit as st
import pandas as pd
import os

# ==============================================================
# CONFIGURACIÓN
# ==============================================================

st.set_page_config(
    page_title="Employee Data Dashboard",
    page_icon="📊",
    layout="wide"
)

# ==============================================================
# CARGA DEL DATASET OFICIAL
# ==============================================================

ruta_datos = os.path.join(
    os.path.dirname(__file__),
    "../datos/employee_data_limpio.csv"
)

df = pd.read_csv(ruta_datos)

# Normalizar espacios en la columna de género
df["gender"] = df["gender"].str.strip()

# ==============================================================
# LOGOTIPO
# ==============================================================

ruta_logo = os.path.join(
    os.path.dirname(__file__),
    "logo_empresa.png"
)

if os.path.exists(ruta_logo):
    st.image(ruta_logo, width=180)

# ==============================================================
# TÍTULO Y DESCRIPCIÓN
# ==============================================================

st.title("Employee Data Dashboard")

st.write(
    "Dashboard interactivo para el análisis de información "
    "relacionada con empleados, desempeño, horas trabajadas "
    "y características laborales."
)

st.divider()

# ==============================================================
# FILTROS
# ==============================================================

st.subheader("Filtros de análisis")

col1, col2, col3 = st.columns(3)

# --------------------------------------------------------------
# GÉNERO
# --------------------------------------------------------------

with col1:

    generos = sorted(
        df["gender"].dropna().unique()
    )

    genero_seleccionado = st.multiselect(
        "Seleccionar género",
        options=generos,
        default=generos
    )

# --------------------------------------------------------------
# PUNTAJE DE DESEMPEÑO
# --------------------------------------------------------------

with col2:

    puntaje_min = int(
        df["performance_score"].min()
    )

    puntaje_max = int(
        df["performance_score"].max()
    )

    rango_desempeno = st.slider(
        "Rango de puntaje de desempeño",
        min_value=puntaje_min,
        max_value=puntaje_max,
        value=(puntaje_min, puntaje_max),
        step=1
    )

# --------------------------------------------------------------
# ESTADO CIVIL
# --------------------------------------------------------------

with col3:

    estados_civiles = sorted(
        df["marital_status"].dropna().unique()
    )

    estado_civil_seleccionado = st.multiselect(
        "Seleccionar estado civil",
        options=estados_civiles,
        default=estados_civiles
    )

# ==============================================================
# APLICACIÓN DE FILTROS
# ==============================================================

df_filtrado = df[
    df["gender"].isin(genero_seleccionado)
    &
    df["performance_score"].between(
        rango_desempeno[0],
        rango_desempeno[1]
    )
    &
    df["marital_status"].isin(
        estado_civil_seleccionado
    )
].copy()

# ==============================================================
# VALIDACIÓN DEL FILTRO
# ==============================================================

st.write(
    f"**Empleados incluidos en el análisis:** {len(df_filtrado)}"
)

if df_filtrado.empty:

    st.warning(
        "No existen registros que cumplan con los filtros seleccionados."
    )

    st.stop()

st.divider()

# ==============================================================
# GRÁFICO 1
# DISTRIBUCIÓN DE LOS PUNTAJES DE DESEMPEÑO
# ==============================================================

st.subheader(
    "Distribución de los puntajes de desempeño"
)

distribucion_desempeno = (
    df_filtrado["performance_score"]
    .value_counts()
    .sort_index()
)

st.bar_chart(
    distribucion_desempeno
)

st.divider()

# ==============================================================
# GRÁFICO 2
# PROMEDIO DE HORAS TRABAJADAS POR GÉNERO
# ==============================================================

st.subheader(
    #"Promedio de horas mensuales trabajadas por género"
    "Promedio de horas trabajadas por género"
)

horas_por_genero = (
    df_filtrado
    .groupby("gender")["average_work_hours"]
    .mean()
    #round(2)
)

st.bar_chart(
    horas_por_genero
)

st.divider()

# ==============================================================
# GRÁFICO 3
# EDAD DE LOS EMPLEADOS VS SALARIO
# ==============================================================

st.subheader(
    "Edad de los empleados con respecto al salario"
)

edad_salario = (
    df_filtrado[
        ["age", "salary"]
    ]
    .dropna()
    .sort_values("age")
)

st.scatter_chart(
    edad_salario,
    x="age",
    y="salary"
)

st.divider()

# ==============================================================
# GRÁFICO 4
# PROMEDIO DE HORAS TRABAJADAS VS PUNTAJE DE DESEMPEÑO
# ==============================================================

st.subheader(
    "Promedio de horas trabajadas vs. puntaje de desempeño"
)

horas_vs_desempeno = (
    df_filtrado
    .groupby("performance_score")["average_work_hours"]
    .mean()
    .round(2)
    .reset_index()
)

#st.write("Datos utilizados en la gráfica:", horas_vs_desempeno)

st.line_chart(
    #horas_vs_desempeno.set_index("performance_score")
    horas_vs_desempeno,
    x="performance_score",
    y="average_work_hours"
)

st.divider()

# ==============================================================
# CONCLUSIÓN
# ==============================================================

st.subheader("Conclusión del análisis")

# --------------------------------------------------------------
# CÁLCULOS PARA LA CONCLUSIÓN
# --------------------------------------------------------------

promedio_horas = (
    df_filtrado["average_work_hours"].mean()
)

promedio_desempeno = (
    df_filtrado["performance_score"].mean()
)

promedio_salario = (
    df_filtrado["salary"].mean()
)

edad_promedio = (
    df_filtrado["age"].mean()
)

genero_mas_frecuente = (
    df_filtrado["gender"]
    .value_counts()
    .idxmax()
)

# --------------------------------------------------------------
# CONCLUSIÓN DINÁMICA
# --------------------------------------------------------------

st.write(
    f"""
    El análisis considera **{len(df_filtrado)} empleados** después
    de aplicar los filtros seleccionados.

    El **puntaje promedio de desempeño** es de
    **{promedio_desempeno:.2f}**, mientras que el promedio de
    **horas mensuales trabajadas** es de
    **{promedio_horas:.2f} horas**.

    La **edad promedio** de los empleados analizados es de
    **{edad_promedio:.1f} años** y el **salario promedio** es de
    **${promedio_salario:,.2f}**.

    El género con mayor representación dentro de la selección
    actual es **{genero_mas_frecuente}**.

    En conjunto, los gráficos permiten analizar la distribución
    del desempeño, comparar las horas trabajadas entre géneros
    y explorar la relación entre edad, salario, horas trabajadas
    y desempeño.
    """
)

# ==============================================================
# PIE DE PÁGINA
# ==============================================================

st.divider()

st.caption(
    "Dashboard desarrollado como parte del reto de análisis "
    "de Employee Data."
)
