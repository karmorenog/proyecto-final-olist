
import streamlit as st
import pandas as pd
from pathlib import Path

# --------------------------------------------------
# CONFIGURACIÓN
# --------------------------------------------------

st.title("📈 Pronóstico de pedidos")
st.markdown(
    """
    Esta sección presenta el pronóstico de pedidos diarios
    para junio de 2018, junto con un intervalo estimado
    para cada día.
    """
)

# --------------------------------------------------
# CARGA DEL ARCHIVO
# --------------------------------------------------

CARPETA_APP = Path(__file__).resolve().parent.parent
CARPETA_REPO = CARPETA_APP.parent

# Buscar el archivo primero en app y luego en la raíz
RUTAS_POSIBLES = [
    CARPETA_APP / "pronostico_junio.csv",
    CARPETA_REPO / "pronostico_junio.csv",
]

RUTA_CSV = next(
    (ruta for ruta in RUTAS_POSIBLES if ruta.exists()),
    None
)

if RUTA_CSV is None:
    st.error(
        "No se encontró pronostico_junio.csv. "
        "Sube el archivo dentro de la carpeta app "
        "o en la raíz del repositorio."
    )
    st.stop()

try:
    df = pd.read_csv(RUTA_CSV)
except Exception as error:
    st.error(f"No fue posible leer el archivo: {error}")
    st.stop()


# --------------------------------------------------
# VALIDACIÓN DE DATOS
# --------------------------------------------------

COLUMNAS_REQUERIDAS = [
    "fecha",
    "pronostico",
    "bajo",
    "alto",
]

faltantes = [
    columna for columna in COLUMNAS_REQUERIDAS
    if columna not in df.columns
]

if faltantes:
    st.error(
        f"Faltan columnas en el archivo: {faltantes}"
    )
    st.stop()

df["fecha"] = pd.to_datetime(
    df["fecha"], errors="coerce"
)

for columna in ["pronostico", "bajo", "alto"]:
    df[columna] = pd.to_numeric(
        df[columna], errors="coerce"
    )

df = df.dropna(
    subset=["fecha", "pronostico", "bajo", "alto"]
).copy()

df = df.sort_values("fecha")

if df.empty:
    st.error("No existen datos válidos para mostrar.")
    st.stop()

if (df["bajo"] > df["alto"]).any():
    st.error(
        "Hay registros donde el límite inferior supera "
        "el límite superior."
    )
    st.stop()


# --------------------------------------------------
# INDICADORES PRINCIPALES
# --------------------------------------------------

total_dias = len(df)
pronostico_total = df["pronostico"].sum()
promedio_diario = df["pronostico"].mean()

dia_maximo = df.loc[
    df["pronostico"].idxmax()
]

st.subheader("Resumen del pronóstico")

col1, col2, col3 = st.columns(3)

col1.metric(
    "Días pronosticados",
    f"{total_dias}"
)

col2.metric(
    "Pronóstico total de junio",
    f"{pronostico_total:,.0f} pedidos"
)

col3.metric(
    "Promedio diario",
    f"{promedio_diario:,.1f} pedidos"
)

st.caption(
    f"El mayor pronóstico diario es de "
    f"{dia_maximo['pronostico']:.0f} pedidos, "
    f"el {dia_maximo['fecha'].strftime('%d/%m/%Y')}."
)


# --------------------------------------------------
# GRÁFICA DEL PRONÓSTICO
# --------------------------------------------------

st.divider()

st.subheader("Pronóstico diario e intervalo estimado")

st.markdown(
    """
    La línea central representa el número estimado de pedidos.
    Las líneas inferior y superior muestran los límites del
    intervalo estimado del 80%.
    """
)

grafica = (
    df.set_index("fecha")[
        ["bajo", "pronostico", "alto"]
    ]
    .rename(
        columns={
            "bajo": "Límite inferior",
            "pronostico": "Pronóstico",
            "alto": "Límite superior",
        }
    )
)

st.line_chart(
    grafica,
    height=420,
    use_container_width=True
)

st.caption(
    "Los límites corresponden al intervalo estimado para cada día, "
    "no a una garantía de que el valor real estará dentro del rango."
)


# --------------------------------------------------
# TABLA DE RESULTADOS
# --------------------------------------------------

st.divider()

st.subheader("Detalle del pronóstico por fecha")

tabla = df.copy()

tabla["fecha"] = tabla["fecha"].dt.strftime("%d/%m/%Y")

tabla = tabla.rename(
    columns={
        "fecha": "Fecha",
        "pronostico": "Pedidos estimados",
        "bajo": "Límite inferior",
        "alto": "Límite superior",
    }
)

st.dataframe(
    tabla.style.format(
        {
            "Pedidos estimados": "{:,.2f}",
            "Límite inferior": "{:,.2f}",
            "Límite superior": "{:,.2f}",
        }
    ),
    use_container_width=True,
    hide_index=True
)


# --------------------------------------------------
# METODOLOGÍA Y EVALUACIÓN
# --------------------------------------------------

st.divider()

st.subheader("Metodología")

st.markdown(
    """
    Para realizar el pronóstico se utilizó un método basado
    en el promedio de las últimas ocho observaciones disponibles
    correspondientes al mismo día de la semana.

    El intervalo estimado del 80% se construyó utilizando
    los errores observados durante la validación temporal.
    """
)

st.subheader("Evaluación del modelo")

col1, col2 = st.columns(2)

col1.metric(
    "MAE en validación temporal",
    "44.38 pedidos/día"
)

col2.metric(
    "Días utilizados en validación",
    "60 días"
)

st.info(
    """
    El MAE representa el error absoluto medio del pronóstico
    en el periodo de validación.

    La comparación contra el pronóstico ingenuo semanal debe
    revisarse por separado para determinar cuál de los dos
    métodos presenta menor error.
    """
)

st.subheader("Interpretación para el negocio")

st.markdown(
    f"""
    El pronóstico estima un promedio de aproximadamente
    **{promedio_diario:.0f} pedidos diarios** durante junio de 2018.

    Esta información puede apoyar la planificación de la demanda,
    la asignación de recursos operativos y la preparación de la
    capacidad necesaria para atender los pedidos.

    Sin embargo, el método se basa en patrones históricos y puede
    no anticipar cambios repentinos en la demanda o tendencias
    nuevas.
    """
)
