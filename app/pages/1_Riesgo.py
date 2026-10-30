
import streamlit as st
import requests

st.title("📊 Evaluación de riesgo de malas reseñas")

st.write(
    "Ingresa las características del pedido para evaluar "
    "su probabilidad de recibir una mala reseña."
)

API_URL = st.secrets.get(
    "API_URL",
    "https://api-riesgo-olist.onrender.com"
)

st.subheader("Datos del pedido")

col1, col2 = st.columns(2)

with col1:
    precio = st.number_input(
        "Precio del pedido",
        min_value=0.0,
        value=100.0,
        step=10.0
    )

    costo_flete = st.number_input(
        "Costo del flete",
        min_value=0.0,
        value=15.0,
        step=5.0
    )

with col2:
    dias_entrega = st.number_input(
        "Días de entrega",
        min_value=0,
        value=10,
        step=1
    )

    cantidad_items = st.number_input(
        "Cantidad de artículos",
        min_value=1,
        value=1,
        step=1
    )

if st.button("Evaluar riesgo", type="primary"):

    datos = {
        "precio": precio,
        "costo_flete": costo_flete,
        "dias_entrega": dias_entrega,
        "cantidad_items": cantidad_items
    }

    try:
        respuesta = requests.post(
            f"{API_URL}/riesgo",
            json=datos,
            timeout=30
        )

        respuesta.raise_for_status()
        resultado = respuesta.json()

        st.subheader("Resultado de la evaluación")

        st.metric(
            "Probabilidad de mala reseña",
            f"{resultado['probabilidad']:.2%}"
        )

        if resultado["riesgo_alto"]:
            st.error("Riesgo alto de recibir una mala reseña")
        else:
            st.success("Riesgo bajo de recibir una mala reseña")

        st.caption(
            f"Umbral de riesgo: {resultado['umbral_riesgo']:.2%}"
        )

    except requests.exceptions.RequestException as error:
        st.error(
            "No fue posible conectar con la API. "
            "Verifica que el servicio esté disponible."
        )
        st.caption(str(error))

