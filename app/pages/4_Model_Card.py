
import streamlit as st
from pathlib import Path

# --------------------------------------------------
# CONFIGURACIÓN
# --------------------------------------------------

st.title("📋 Ficha del modelo")
st.markdown(
    """
    Información sobre el propósito, los datos, el desempeño,
    las limitaciones y el uso responsable del modelo de riesgo
    de malas reseñas.
    """
)

# --------------------------------------------------
# UBICACIÓN DEL ARCHIVO
# --------------------------------------------------

CARPETA_APP = Path(__file__).resolve().parent.parent
RUTA_FICHA = CARPETA_APP / "ficha_modelo.md"

# --------------------------------------------------
# MOSTRAR FICHA
# --------------------------------------------------

if not RUTA_FICHA.exists():

    st.error(
        "No se encontró ficha_modelo.md. "
        "Verifica que esté guardado directamente dentro de la carpeta app."
    )

else:

    try:
        contenido = RUTA_FICHA.read_text(encoding="utf-8")

        st.markdown(contenido)

    except Exception as error:

        st.error(
            f"No fue posible cargar la ficha del modelo: {error}"
        )

# --------------------------------------------------
# INFORMACIÓN DEL UMBRAL
# --------------------------------------------------

st.divider()

st.subheader("Configuración del riesgo")

col1, col2 = st.columns(2)

col1.metric(
    "Umbral de riesgo",
    "25.97%"
)

col2.metric(
    "Criterio de clasificación",
    "Probabilidad ≥ umbral"
)

st.caption(
    "El umbral se utiliza en la API para identificar los pedidos "
    "que deben marcarse como riesgo alto."
)

st.info(
    """
    **Uso responsable:** el modelo debe apoyar la priorización
    de llamadas de atención al cliente. Las predicciones deben
    revisarse antes de tomar decisiones y no deben utilizarse
    para penalizar automáticamente a vendedores.
    """
)
