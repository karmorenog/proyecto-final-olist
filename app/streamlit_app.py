
import streamlit as st
import pandas as pd
import requests
from pathlib import Path

# --------------------------------------------------
# CONFIGURACIÓN GENERAL
# --------------------------------------------------

st.set_page_config(
    page_title="Olist - Análisis de riesgo",
    page_icon="📦",
    layout="wide"
)

API_URL = st.secrets.get(
    "API_URL",
    "https://api-riesgo-olist.onrender.com"
)

BASE_DIR = Path(__file__).resolve().parent

# --------------------------------------------------
# MENÚ DE NAVEGACIÓN
# --------------------------------------------------

paginas = st.navigation([
    st.Page("streamlit_app.py", title="Inicio", icon="🏠"),
    st.Page("pages/1_Riesgo.py", title="Riesgo de pedidos", icon="📊"),
    st.Page("pages/2_Comentarios.py", title="Comentarios", icon="💬"),
    st.Page("pages/3_Pronostico.py", title="Pronóstico", icon="📈"),
    st.Page("pages/4_Model_Card.py", title="Model Card", icon="📋")
])

# --------------------------------------------------
# PÁGINA DE INICIO
# --------------------------------------------------

st.title("📦 Olist - Plataforma de análisis")
st.subheader("Análisis de riesgo de malas reseñas y pronóstico de pedidos")

st.markdown("""
Bienvenido a la plataforma de análisis del proyecto Olist.

Esta aplicación integra herramientas para:

- Evaluar el riesgo de malas reseñas de los pedidos.
- Explorar los resultados del análisis de comentarios.
- Consultar el pronóstico diario de pedidos de junio de 2018.
- Revisar la documentación del modelo predictivo.
""")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.metric("Pronóstico", "Junio 2018")

with col2:
    st.metric("API", "FastAPI + Render")

st.info("Selecciona una sección en el menú lateral para comenzar.")

paginas.run()
