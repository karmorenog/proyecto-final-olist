
import streamlit as st

# --------------------------------------------------
# CONFIGURACIÓN GENERAL
# --------------------------------------------------

st.set_page_config(
    page_title="Olist - Plataforma de análisis",
    page_icon="📦",
    layout="wide"
)

# --------------------------------------------------
# PÁGINA PRINCIPAL
# --------------------------------------------------

st.title("📦 Olist - Plataforma de análisis")

st.subheader(
    "Análisis de riesgo de malas reseñas y pronóstico de pedidos"
)

st.markdown(
    """
    Bienvenido a la plataforma de análisis del proyecto Olist.

    Esta aplicación integra cuatro herramientas:

    - **Riesgo de pedidos:** estima la probabilidad de recibir una mala reseña.
    - **Comentarios:** compara el sentimiento del texto con las estrellas.
    - **Pronóstico:** presenta la estimación de pedidos diarios de junio de 2018.
    - **Ficha del modelo:** explica el funcionamiento, las limitaciones y el uso responsable del modelo.
    """
)

st.info(
    "Selecciona una de las cuatro secciones en el menú lateral."
)

# --------------------------------------------------
# NAVEGACIÓN ENTRE PÁGINAS
# --------------------------------------------------

paginas = st.navigation(
    [
        st.Page(
            "pages/1_Riesgo.py",
            title="Riesgo de pedidos",
            icon="📊"
        ),
        st.Page(
            "pages/2_Comentarios.py",
            title="Comentarios",
            icon="💬"
        ),
        st.Page(
            "pages/3_Pronostico.py",
            title="Pronóstico",
            icon="📈"
        ),
        st.Page(
            "pages/4_Model_Card.py",
            title="Ficha del modelo",
            icon="📋"
        ),
    ]
)

paginas.run()
