
# Ficha del modelo – Predicción de riesgo de malas reseñas

## 1. Propósito del modelo

El modelo tiene como objetivo estimar la probabilidad de que un pedido de Olist reciba una mala reseña, definida como una calificación de 1 o 2 estrellas.

Su propósito es apoyar al equipo de atención al cliente para priorizar los pedidos que podrían requerir seguimiento después de la entrega.

El modelo debe utilizarse como una herramienta de apoyo a la toma de decisiones. No debe utilizarse para sancionar automáticamente a vendedores, rechazar pedidos o tomar decisiones sin revisión humana.

## 2. Datos utilizados

**Fuente:** Base de datos pública de Olist, utilizada en el proyecto a través del esquema `final` del curso.

**Periodo:** Datos históricos de Olist correspondientes al periodo 2016–2018 disponible en la base de datos del proyecto.

**Cantidad:** La tabla del contrato contiene 77,304 pedidos entregados y con reseña.

**Variable objetivo:** `mala_resena`, donde:
- 1 representa una reseña de 1 o 2 estrellas.
- 0 representa una reseña de 3, 4 o 5 estrellas.

El modelo utiliza información disponible al momento de la entrega, como fechas del pedido, características de los artículos, pagos y ubicación geográfica.

Se excluyen el texto de los comentarios, la longitud de los comentarios y las fechas relacionadas con la reseña, porque esa información no está disponible en el momento en que se realiza la predicción. Utilizarla produciría fuga de información.

## 3. Desempeño del modelo

La evaluación principal del proyecto utiliza validación temporal: se entrena con pedidos más antiguos y se evalúa con pedidos más recientes.

La métrica principal es la **precisión en el 10% de mayor riesgo**, que representa qué proporción de los pedidos seleccionados para seguimiento realmente termina con una mala reseña.

El modelo también debe compararse con dos referencias:
- Selección al azar, utilizando la tasa de malas reseñas del periodo de validación.
- Regla del retraso, priorizando los pedidos con mayor retraso frente a la fecha prometida.

**Umbral de riesgo configurado en la API:** 25.97%.

La API clasifica un pedido como de riesgo alto cuando su probabilidad estimada alcanza o supera este umbral.

**Resultados cuantitativos de validación:** las cifras exactas de precisión en el 10%, tasa de referencia al azar y precisión de la regla del retraso deben incorporarse desde las salidas del notebook de evaluación. No se incluyen aquí porque no están disponibles en los archivos de despliegue revisados.

## 4. Limitaciones conocidas

El modelo puede presentar errores en situaciones como:

- Cambios en los patrones de compra o comportamiento de los clientes.
- Variaciones en la logística, tiempos de entrega o desempeño de los vendedores.
- Periodos con pocos retrasos o condiciones diferentes a las observadas durante el entrenamiento.
- Pedidos con características poco frecuentes o información incompleta.
- Cambios en la calidad de los datos de entrada.

La probabilidad estimada no garantiza que un pedido recibirá una mala reseña.

Además, el desempeño observado durante la validación histórica puede cambiar cuando el modelo se utiliza con pedidos de periodos futuros.

## 5. Impacto de los errores

**Falso positivo:** el modelo identifica un pedido como riesgoso, pero el cliente termina dejando una buena reseña. Esto puede ocasionar llamadas innecesarias y consumo de recursos del equipo de atención al cliente.

**Falso negativo:** el modelo clasifica un pedido como de bajo riesgo, pero el cliente termina dejando una mala reseña. Se podría perder una oportunidad de contactar al cliente y resolver el problema.

**Posible impacto en vendedores:** un retraso no siempre depende directamente del vendedor. Por ello, el modelo no debe utilizarse para penalizar vendedores automáticamente, ya que podrían verse afectados por problemas logísticos o circunstancias fuera de su control.

## 6. Recomendaciones de uso y supervisión

Se recomienda utilizar el modelo para priorizar el seguimiento de los pedidos con mayor probabilidad de recibir malas reseñas.

La decisión de contactar al cliente debe mantenerse bajo supervisión humana.

También se recomienda:
- Revisar periódicamente los resultados reales frente a las predicciones.
- Monitorear los cambios en las tasas de malas reseñas y en los tiempos de entrega.
- Evaluar nuevamente el modelo cuando existan cambios importantes en los datos o en la operación.
- Revisar el umbral de riesgo cuando cambie la capacidad de atención al cliente.
- Evitar utilizar las predicciones como único criterio para tomar decisiones sobre vendedores o clientes.

El modelo debe considerarse una herramienta de apoyo y no un sustituto del criterio del equipo de atención al cliente.
