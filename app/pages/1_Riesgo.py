
import streamlit as st
import requests
import pandas as pd

st.set_page_config(
    page_title="Riesgo de pedidos - Olist",
    page_icon="📊",
    layout="wide"
)

API_URL = st.secrets.get(
    "API_URL",
    "https://api-riesgo-olist.onrender.com"
)

st.title("📊 Evaluación de riesgo de malas reseñas")

st.write(
    "Ingresa la información de un pedido para estimar "
    "su probabilidad de recibir una mala reseña."
)

st.info(
    "La predicción se realiza considerando la información "
    "del pedido al momento de su entrega."
)

st.subheader("1. Fechas del pedido")

col1, col2 = st.columns(2)

with col1:
    fecha_compra = st.date_input(
        "Fecha de compra",
        value=pd.to_datetime("2018-05-01")
    )

    fecha_aprobacion = st.date_input(
        "Fecha de aprobación",
        value=pd.to_datetime("2018-05-01")
    )

    fecha_transportista = st.date_input(
        "Fecha de entrega al transportista",
        value=pd.to_datetime("2018-05-02")
    )

with col2:
    fecha_entrega = st.date_input(
        "Fecha de entrega al cliente",
        value=pd.to_datetime("2018-05-10")
    )

    fecha_estimada = st.date_input(
        "Fecha estimada de entrega",
        value=pd.to_datetime("2018-05-12")
    )

st.subheader("2. Información del cliente y vendedor")

col1, col2 = st.columns(2)

with col1:
    estado_cliente = st.text_input(
        "Estado del cliente",
        value="SP"
    )

    estado_vendedor = st.text_input(
        "Estado del vendedor",
        value="SP"
    )

    categoria = st.text_input(
        "Categoría del producto",
        value="cama_mesa_banho"
    )

with col2:
    tipo_pago = st.selectbox(
        "Tipo de pago",
        ["credit_card", "boleto", "voucher", "debit_card", "not_defined"]
    )

st.subheader("3. Características del pedido")

col1, col2, col3 = st.columns(3)

with col1:
    n_items = st.number_input(
        "Cantidad de artículos",
        min_value=1,
        value=1
    )

    n_vendedores = st.number_input(
        "Cantidad de vendedores",
        min_value=1,
        value=1
    )

with col2:
    precio_total = st.number_input(
        "Precio total",
        min_value=0.0,
        value=100.0
    )

    flete_total = st.number_input(
        "Costo total del flete",
        min_value=0.0,
        value=15.0
    )

with col3:
    peso_total_g = st.number_input(
        "Peso total (gramos)",
        min_value=0.0,
        value=1000.0
    )

    fotos_promedio = st.number_input(
        "Promedio de fotos",
        min_value=0.0,
        value=2.0
    )

cuotas_max = st.number_input(
    "Máximo de cuotas",
    min_value=0,
    value=1
)

st.divider()

if st.button("Evaluar riesgo del pedido", type="primary"):

    pedido = {
        "order_purchase_timestamp": str(fecha_compra),
        "order_approved_at": str(fecha_aprobacion),
        "order_delivered_carrier_date": str(fecha_transportista),
        "order_delivered_customer_date": str(fecha_entrega),
        "order_estimated_delivery_date": str(fecha_estimada),
        "estado_cliente": estado_cliente,
        "n_items": n_items,
        "n_vendedores": n_vendedores,
        "precio_total": precio_total,
        "flete_total": flete_total,
        "peso_total_g": peso_total_g,
        "fotos_promedio": fotos_promedio,
        "categoria": categoria,
        "estado_vendedor": estado_vendedor,
        "tipo_pago": tipo_pago,
        "cuotas_max": cuotas_max
    }

    try:
        respuesta = requests.post(
            f"{API_URL}/riesgo",
            json=pedido,
            timeout=60
        )

        respuesta.raise_for_status()
        resultado = respuesta.json()

        st.subheader("Resultado de la evaluación")

        st.metric(
            "Probabilidad de mala reseña",
            f"{resultado['probabilidad']:.2%}"
        )

        if resultado["riesgo_alto"]:
            st.error("⚠️ Riesgo alto de mala reseña")
        else:
            st.success("✅ Riesgo bajo de mala reseña")

        st.caption(
            f"Umbral de riesgo: {resultado['umbral_riesgo']:.2%}"
        )

    except requests.exceptions.RequestException as error:
        st.error(
            "No fue posible conectar con la API. "
            "Verifica que el servicio esté disponible."
        )
        st.caption(str(error))
