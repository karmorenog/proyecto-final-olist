
import streamlit as st
import pandas as pd
from pathlib import Path

# --------------------------------------------------
# CONFIGURACIÓN Y CARGA DE DATOS
# --------------------------------------------------

st.title("💬 Análisis de sentimientos de comentarios")
st.markdown(
    """
    Esta sección compara el sentimiento expresado por los clientes
    en sus comentarios con el sentimiento asociado a las estrellas
    que calificaron en sus pedidos.
    """
)

# Ubicación del CSV dentro de la carpeta app
RUTA_CSV = (
    Path(__file__).resolve().parent.parent
    / "resultados_sentimiento.csv"
)

if not RUTA_CSV.exists():
    st.error(
        "No se encontró resultados_sentimiento.csv. "
        "Verifica que el archivo esté dentro de la carpeta app."
    )
    st.stop()

try:
    df = pd.read_csv(RUTA_CSV)
except Exception as error:
    st.error(f"No fue posible leer el archivo: {error}")
    st.stop()


# --------------------------------------------------
# VALIDACIÓN DE COLUMNAS
# --------------------------------------------------

COLUMNAS_REQUERIDAS = [
    "review_score",
    "review_comment_message",
    "prediccion_modelo",
    "confianza_modelo",
]

faltantes = [
    columna for columna in COLUMNAS_REQUERIDAS
    if columna not in df.columns
]

if faltantes:
    st.error(
        f"Faltan estas columnas en el CSV: {faltantes}"
    )
    st.stop()


# --------------------------------------------------
# LIMPIEZA Y PREPARACIÓN
# --------------------------------------------------

df["review_score"] = pd.to_numeric(
    df["review_score"], errors="coerce"
)

df["confianza_modelo"] = pd.to_numeric(
    df["confianza_modelo"], errors="coerce"
)

df["review_comment_message"] = (
    df["review_comment_message"]
    .fillna("")
    .astype(str)
    .str.strip()
)

# Normalizar las etiquetas del modelo
MAPA_SENTIMIENTOS = {
    "positivo": "positivo",
    "positive": "positivo",
    "neutral": "neutral",
    "negativo": "negativo",
    "negative": "negativo",
}

df["prediccion_modelo"] = (
    df["prediccion_modelo"]
    .astype(str)
    .str.lower()
    .str.strip()
    .map(MAPA_SENTIMIENTOS)
)

# Agrupar las estrellas según las instrucciones:
# 1-2 negativo, 3 neutral, 4-5 positivo
def agrupar_estrellas(valor):
    if pd.isna(valor):
        return None
    if valor in [1, 2]:
        return "negativo"
    if valor == 3:
        return "neutral"
    if valor in [4, 5]:
        return "positivo"
    return None


df["sentimiento_estrellas"] = (
    df["review_score"].apply(agrupar_estrellas)
)

# Conservar únicamente registros válidos
total_original = len(df)

df = df.dropna(
    subset=[
        "sentimiento_estrellas",
        "prediccion_modelo",
    ]
).copy()

df = df[
    df["review_comment_message"] != ""
].copy()

if df.empty:
    st.error("No hay comentarios válidos para mostrar.")
    st.stop()

if len(df) < total_original:
    st.warning(
        f"Se omitieron {total_original - len(df):,} "
        "registros incompletos o inválidos."
    )


# --------------------------------------------------
# MÉTRICAS PRINCIPALES
# --------------------------------------------------

df["coincide"] = (
    df["sentimiento_estrellas"]
    == df["prediccion_modelo"]
)

total_comentarios = len(df)
coincidencia = df["coincide"].mean()
desacuerdos = df[~df["coincide"]].copy()
porcentaje_desacuerdo = len(desacuerdos) / total_comentarios

confianza_promedio = df["confianza_modelo"].mean()

st.subheader("Indicadores generales")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Comentarios analizados",
    f"{total_comentarios:,}"
)

col2.metric(
    "Coincidencia",
    f"{coincidencia:.1%}"
)

col3.metric(
    "Desacuerdos",
    f"{len(desacuerdos):,}"
)

col4.metric(
    "Confianza promedio",
    f"{confianza_promedio:.1%}"
    if pd.notna(confianza_promedio)
    else "No disponible"
)

st.caption(
    "La coincidencia mide qué proporción de comentarios "
    "recibió la misma clasificación según las estrellas y el modelo."
)


# --------------------------------------------------
# TABLA CRUZADA
# --------------------------------------------------

st.divider()
st.subheader("Comparación: estrellas vs. sentimiento del modelo")

st.markdown(
    """
    Las estrellas se agrupan en tres categorías:
    - **1 y 2 estrellas:** Negativo
    - **3 estrellas:** Neutral
    - **4 y 5 estrellas:** Positivo
    """
)

orden = ["negativo", "neutral", "positivo"]

tabla = pd.crosstab(
    df["sentimiento_estrellas"],
    df["prediccion_modelo"]
).reindex(
    index=orden,
    columns=orden,
    fill_value=0
)

tipo_tabla = st.selectbox(
    "Formato de la tabla",
    [
        "Cantidad de comentarios",
        "Porcentaje dentro de cada grupo de estrellas",
    ]
)

if tipo_tabla == "Cantidad de comentarios":

    tabla_mostrar = tabla.copy()

    tabla_mostrar["Total"] = tabla_mostrar.sum(axis=1)

    tabla_mostrar.loc["Total"] = tabla_mostrar.sum(axis=0)

    st.dataframe(
        tabla_mostrar,
        use_container_width=True
    )

else:

    tabla_porcentaje = tabla.div(
        tabla.sum(axis=1),
        axis=0
    )

    st.dataframe(
        tabla_porcentaje.style.format("{:.1%}"),
        use_container_width=True
    )


# --------------------------------------------------
# DISTRIBUCIÓN DE SENTIMIENTOS
# --------------------------------------------------

st.subheader("Distribución de sentimientos")

distribucion = pd.DataFrame({
    "Según estrellas": (
        df["sentimiento_estrellas"].value_counts()
    ),
    "Según modelo": (
        df["prediccion_modelo"].value_counts()
    ),
}).reindex(orden).fillna(0).astype(int)

st.bar_chart(distribucion)

st.caption(
    "La gráfica permite observar cómo cambia la distribución "
    "cuando se utiliza el texto del comentario en lugar de las estrellas."
)


# --------------------------------------------------
# EXPLORACIÓN DE DESACUERDOS
# --------------------------------------------------

st.divider()
st.subheader("Exploración de comentarios con desacuerdos")

st.markdown(
    """
    Estos son los casos donde el sentimiento asociado a las estrellas
    no coincide con la predicción del modelo. Revisarlos ayuda a
    identificar comentarios ambiguos, problemas específicos o posibles
    limitaciones de clasificación.
    """
)

if desacuerdos.empty:

    st.success("No se encontraron desacuerdos.")

else:

    opciones = ["Todos"] + sorted(
        (
            desacuerdos["sentimiento_estrellas"]
            + " → "
            + desacuerdos["prediccion_modelo"]
        ).unique().tolist()
    )

    filtro = st.selectbox(
        "Filtrar por tipo de desacuerdo",
        opciones
    )

    if filtro != "Todos":

        sentimiento_estrella, prediccion = filtro.split(" → ")

        datos_filtrados = desacuerdos[
            (desacuerdos["sentimiento_estrellas"] == sentimiento_estrella)
            & (desacuerdos["prediccion_modelo"] == prediccion)
        ].copy()

    else:

        datos_filtrados = desacuerdos.copy()

    st.write(
        f"Comentarios encontrados: {len(datos_filtrados):,}"
    )

    columnas_mostrar = [
        "review_score",
        "sentimiento_estrellas",
        "prediccion_modelo",
        "confianza_modelo",
        "review_comment_message",
    ]

    tabla_desacuerdos = datos_filtrados[
        columnas_mostrar
    ].copy()

    tabla_desacuerdos["confianza_modelo"] = (
        tabla_desacuerdos["confianza_modelo"] * 100
    ).round(1)

    tabla_desacuerdos = tabla_desacuerdos.rename(
        columns={
            "review_score": "Estrellas",
            "sentimiento_estrellas": "Sentimiento según estrellas",
            "prediccion_modelo": "Sentimiento del modelo",
            "confianza_modelo": "Confianza (%)",
            "review_comment_message": "Comentario del cliente",
        }
    )

    st.dataframe(
        tabla_desacuerdos,
        use_container_width=True,
        height=450
    )


# --------------------------------------------------
# CONCLUSIÓN
# --------------------------------------------------

st.divider()
st.subheader("Conclusiones del análisis")

st.markdown(
    f"""
    - Se analizaron **{total_comentarios:,} comentarios**.
    - El sentimiento derivado de las estrellas coincidió con la
      predicción del modelo en **{coincidencia:.1%}** de los casos.
    - En **{len(desacuerdos):,} comentarios ({porcentaje_desacuerdo:.1%})**
      se encontraron diferencias entre ambas clasificaciones.

    Los desacuerdos muestran que las estrellas y el texto no siempre
    transmiten la misma información. Por eso, analizar los comentarios
    puede ayudar a identificar problemas concretos que una calificación
    numérica no explica por sí sola.
    """
)

st.info(
    "Interpretación: las estrellas representan la valoración numérica "
    "del cliente, mientras que el modelo analiza el sentimiento del texto. "
    "Las diferencias deben revisarse antes de tomar decisiones sobre "
    "clientes o vendedores."
)
