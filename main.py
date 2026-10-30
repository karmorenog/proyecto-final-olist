
import sys
import json
from pathlib import Path

import pandas as pd
import numpy as np
import joblib

from fastapi import FastAPI, HTTPException
from preparacion import crear_variables


# ==========================================
# DIAGNOSTICO DE VERSIONES
# ==========================================

print("VERSION PYTHON:", sys.version, flush=True)
print("VERSION PANDAS:", pd.__version__, flush=True)
print("VERSION NUMPY:", np.__version__, flush=True)


# ==========================================
# CARGA DEL MODELO Y UMBRAL
# ==========================================

CARPETA = Path(__file__).resolve().parent

modelo = joblib.load(CARPETA / "modelo_riesgo.joblib")

with open(CARPETA / "umbral_riesgo.json", "r", encoding="utf-8") as archivo:
    umbral = json.load(archivo)["umbral_riesgo"]


# ==========================================
# CONFIGURACION DE FASTAPI
# ==========================================

app = FastAPI(
    title="API de riesgo de malas reseñas",
    description="Predice el riesgo de recibir una reseña de 1 o 2 estrellas.",
    version="1.0.0"
)


# ==========================================
# COLUMNAS REQUERIDAS
# ==========================================

COLUMNAS_REQUERIDAS = [
    "order_purchase_timestamp",
    "order_approved_at",
    "order_delivered_carrier_date",
    "order_delivered_customer_date",
    "order_estimated_delivery_date",
    "estado_cliente",
    "n_items",
    "n_vendedores",
    "precio_total",
    "flete_total",
    "peso_total_g",
    "fotos_promedio",
    "categoria",
    "estado_vendedor",
    "tipo_pago",
    "cuotas_max",
]


# ==========================================
# RUTA PRINCIPAL
# ==========================================

@app.get("/")
def inicio():
    return {
        "mensaje": "API de riesgo de malas reseñas activa",
        "estado": "ok"
    }


# ==========================================
# PREDICCION DE RIESGO
# ==========================================

@app.post("/riesgo")
def predecir_riesgo(pedido: dict):

    print("DIAGNOSTICO 1: solicitud recibida", flush=True)

    faltantes = [
        columna for columna in COLUMNAS_REQUERIDAS
        if columna not in pedido
    ]

    if faltantes:
        raise HTTPException(
            status_code=422,
            detail=f"Faltan columnas requeridas: {faltantes}"
        )

    try:
        print("DIAGNOSTICO 2: creando DataFrame", flush=True)

        datos = pd.DataFrame([pedido])

        print("DIAGNOSTICO 3: preparando variables", flush=True)

        variables = crear_variables(datos)

        print(
            f"DIAGNOSTICO 4: variables listas, forma={variables.shape}",
            flush=True
        )

        print("DIAGNOSTICO 5: ejecutando predict_proba", flush=True)

        probabilidades = modelo.predict_proba(variables)

        print("DIAGNOSTICO 6: prediccion completada", flush=True)

        probabilidad = float(probabilidades[0, 1])

        return {
            "probabilidad": round(probabilidad, 4),
            "riesgo_alto": bool(probabilidad >= umbral),
            "umbral_riesgo": round(float(umbral), 4)
        }

    except HTTPException:
        raise

    except Exception as error:

        print(f"ERROR DE PREDICCION: {error!r}", flush=True)

        raise HTTPException(
            status_code=500,
            detail=f"Error al calcular el riesgo: {str(error)}"
        )
