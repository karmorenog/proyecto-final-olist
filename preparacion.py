
# Preparar variables para el modelo de riesgo

import numpy as np
import pandas as pd


def crear_variables(datos):
    """
    Transforma las columnas del contrato en variables predictoras.
    La predicción se realiza en el momento de la entrega del pedido.
    """

    print("PREPARACION 1: inicio", flush=True)

    datos = datos.copy()
    print("PREPARACION 2: copia de datos completada", flush=True)

    columnas_requeridas = [
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

    faltantes = [
        columna
        for columna in columnas_requeridas
        if columna not in datos.columns
    ]

    if faltantes:
        raise ValueError(
            f"Faltan columnas requeridas del contrato: {faltantes}"
        )

    print("PREPARACION 3: columnas verificadas", flush=True)

    # Convertir fechas
    columnas_fechas = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]

    for columna in columnas_fechas:

        print(
            f"PREPARACION 4: convirtiendo {columna}",
            flush=True
        )

        try:
            valor = datos[columna].iloc[0]

            print(
                f"VALOR RECIBIDO: {valor!r}",
                flush=True
            )

            print(
                f"TIPO RECIBIDO: {type(valor)}",
                flush=True
            )

            datos[columna] = pd.to_datetime(
                datos[columna],
                errors="coerce"
            )

            print(
                f"CONVERSION EXITOSA: {columna}",
                flush=True
            )

        except Exception as error:
            print(
                f"ERROR CONVIRTIENDO {columna}: {error!r}",
                flush=True
            )
            raise

    print("PREPARACION 5: fechas convertidas", flush=True)

    variables = pd.DataFrame(index=datos.index)

    print("PREPARACION 6: DataFrame creado", flush=True)

    # Variables de tiempo
    variables["dias_desde_compra"] = (
        datos["order_delivered_customer_date"]
        - datos["order_purchase_timestamp"]
    ).dt.total_seconds() / 86400

    variables["horas_hasta_aprobacion"] = (
        datos["order_approved_at"]
        - datos["order_purchase_timestamp"]
    ).dt.total_seconds() / 3600

    variables["dias_hasta_transportista"] = (
        datos["order_delivered_carrier_date"]
        - datos["order_approved_at"]
    ).dt.total_seconds() / 86400

    variables["dias_retraso"] = (
        datos["order_delivered_customer_date"]
        - datos["order_estimated_delivery_date"]
    ).dt.total_seconds() / 86400

    variables["mes_compra"] = (
        datos["order_purchase_timestamp"].dt.month
    )

    variables["dia_semana_compra"] = (
        datos["order_purchase_timestamp"].dt.dayofweek
    )

    print("PREPARACION 7: variables de tiempo listas", flush=True)

    # Variables numéricas
    columnas_numericas = [
        "n_items",
        "n_vendedores",
        "precio_total",
        "flete_total",
        "peso_total_g",
        "fotos_promedio",
        "cuotas_max",
    ]

    for columna in columnas_numericas:
        variables[columna] = pd.to_numeric(
            datos[columna],
            errors="coerce"
        )

    print("PREPARACION 8: variables numéricas listas", flush=True)

    # Variables categóricas
    columnas_categoricas = [
        "estado_cliente",
        "categoria",
        "estado_vendedor",
        "tipo_pago",
    ]

    for columna in columnas_categoricas:
        variables[columna] = (
            datos[columna]
            .fillna("Desconocido")
            .astype(str)
        )

    print("PREPARACION 9: variables categóricas listas", flush=True)

    # Evitar valores infinitos
    variables = variables.replace(
        [np.inf, -np.inf],
        np.nan
    )

    print(
        f"PREPARACION 10: proceso completado. "
        f"Filas={variables.shape[0]}, "
        f"columnas={variables.shape[1]}",
        flush=True
    )

    return variables
