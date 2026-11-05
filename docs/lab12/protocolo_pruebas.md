# Lab 12 — Criterios de comparación y protocolo de las tres pruebas

Este documento fija antes de construir el informe final cómo vamos a comparar Dash y Power BI, para que
los criterios y los resultados esperados no se ajusten después a lo que salga. Las pruebas las ejecuta
Nicolás Concuá en la entrega final, sección 5 del enunciado.

## 1. Criterios de la matriz de comparación

La matriz tendrá las columnas criterio, evidencia en Dash, evidencia en Power BI e implicación para la
tarea. Cada celda de evidencia debe apuntar a algo verificable, un archivo del repositorio, una captura,
un tiempo medido o una página de documentación oficial con su fecha de consulta, no a una opinión.

| Criterio | Qué evidencia se recoge en cada versión |
|--|--|
| Facilidad de aprendizaje | Conocimientos que hizo falta tener, Python y callbacks frente a Power Query y DAX, y dudas o bloqueos anotados por cada integrante |
| Tiempo de desarrollo | Horas efectivas de `planificacion.md`, separando el trabajo de datos y documentación |
| Preparación y actualización de datos | Pasos para cargar la base y para actualizarla con un mes nuevo, en `src/data.py` frente a Power Query y Actualizar |
| Integración de resultados de modelos | Cómo entran `predictions.csv` y `metrics.csv` y si se puede volver a generar una predicción, con el resultado de la verificación de indicadores |
| Interacción y navegación | Cuántos enlaces entre gráficos, cómo se cambia el nivel de detalle y cómo se vuelve a la vista inicial, con capturas |
| Personalización | Qué se pudo hacer igual y qué hubo que sustituir, por ejemplo el mapa de calor y el diagrama de caja, sección 6 de `diseno.md` |
| Rendimiento | Tiempo de apertura y de respuesta a un filtro en el mismo equipo, y tamaño del `.pbix` frente al de la aplicación |
| Colaboración y control de versiones | Diferencias legibles en Git del código de Dash frente al `.pbix` binario y cómo se coordinó la edición |
| Requisitos para compartir o desplegar | Qué necesita otra persona para abrir cada versión, sistema operativo, instalación, cuenta y licencia |

Costos y acceso, sección 5.2, se documentan aparte separando tres situaciones, desarrollar y usar en
local, publicar para que otros lo vean y mantener la solución en el tiempo. Para cada versión se anota
el sistema operativo, la licencia, el alojamiento y las restricciones, citando la documentación oficial
de Microsoft y de Plotly con la fecha de consulta. Que Power BI Desktop o Dash sean gratuitos para
desarrollar no implica que distribuir el informe lo sea.

## 2. Condiciones de las pruebas

- Mismos datos en las dos versiones, la base de Migración hasta junio de 2026 y las predicciones del
  Laboratorio 10, commit `27d624b`, y `powerbi/data/` generado con `scripts/export_powerbi.py`.
- Cada prueba empieza desde la vista inicial de la página indicada, después de Restablecer en Power BI y
  de recargar la página en Dash.
- Se cuenta un clic por cada clic, selección o tecla que cambie la vista. Se cronometra desde que la
  página está cargada hasta que la persona dice el resultado en voz alta.
- La misma persona hace las tres pruebas en las dos herramientas. Para no favorecer a la segunda por
  conocer ya la respuesta, en la prueba 1 empieza por Dash, en la 2 por Power BI y en la 3 por Dash.
- Se usa el mismo equipo cuando sea posible. Power BI Desktop solo corre en Windows y Dash se abre en
  el navegador, así que si se usan equipos distintos se anota el sistema operativo, el procesador y la
  memoria de cada uno.
- Se anota la experiencia previa de quien ejecuta con cada herramienta.

## 3. Prueba 1. Responder una pregunta de gestión con filtros

Pregunta, P2. En 2025, ¿en qué mes llegaron más visitantes por vía terrestre y cuántos fueron? ¿Cuál
fue el mes más bajo?

| | Dash, Lab 10 | Power BI |
|--|--|--|
| Página de inicio | Panorama | Panorama |
| Pasos | Desmarcar Aérea y Marítima en Vías. Clic en la barra de 2025 en V1. Leer en V2 el punto más alto y el más bajo con el tooltip | Dejar solo Terrestre en el segmentador de vía. Clic en la columna de 2025 en V1. Leer en V2 el punto más alto y el más bajo con la información sobre herramientas |

Resultado esperado. Diciembre, 238,290 visitantes terrestres. El mes más bajo es septiembre con
147,654.

## 4. Prueba 2. Pasar de la vista general al detalle y regresar

Pregunta, P3 y P4. En 2025, ¿qué peso tiene El Salvador entre los visitantes extranjeros y por qué punto
entra la mayoría de ellos? Al terminar, volver a la vista de todas las regiones.

| | Dash, Lab 10 | Power BI |
|--|--|--|
| Página de inicio | Mercados y fronteras, años 2025 a 2025 | Mercados y fronteras con el año 2025 |
| Pasos | Clic en América Del Centro en el treemap V5. Clic en El Salvador. Leer su porcentaje en V5 y el primer punto en V6. Clic en la barra superior del treemap hasta volver a Todas las regiones | Clic derecho en El Salvador dentro de V5 o V3 y Obtener detalles. Leer porcentaje y primer punto de ingreso en la página Detalle de país. Botón Volver y Restablecer. Alternativa, drill down en V5 de región a país y drill up para volver |

Resultado esperado. El Salvador aporta 1,582,845 visitantes, el 47 % de los extranjeros de 2025. Su
principal punto de ingreso es Valle Nuevo, con el 39 % de sus llegadas. Al regresar, V5 vuelve a mostrar
las regiones y V6 todos los puntos de ingreso, con Valle Nuevo como primero, 31 % de América del Centro.

## 5. Prueba 3. Consultar las predicciones y comparar los tres modelos

Pregunta, P5. Para la serie Aérea, ¿qué modelo se equivoca menos en el conjunto de prueba, cuánto en
promedio, y en qué mes del año falla más el Holt-Winters?

| | Dash, Lab 10 | Power BI |
|--|--|--|
| Página de inicio | Pronósticos | Pronósticos |
| Pasos | Elegir la serie Aérea. Leer el primer modelo de la tabla de errores. En V9 ubicar la barra más alta del Holt-Winters | Elegir Aérea en el selector de serie. Leer la tabla de métricas. En V9 ubicar la columna más alta del Holt-Winters |

Resultado esperado. El ARIMA(1,1,1) tiene el menor error, MAE de 33,226 visitantes por mes y MAPE de
33.3 %, medidos en el conjunto de prueba de abril de 2021 a junio de 2026, 63 meses. El Holt-Winters
falla más en julio, con un error medio de unos 60,048 visitantes. Las métricas solo se comparan entre
modelos de la misma serie, no entre series.

## 6. Registro de cada prueba

Cada ejecución se anota en esta tabla y se acompaña con una captura del resultado en
`docs/lab12/evidencia/`.

| Prueba | Herramienta | Resultado obtenido | ¿Coincide? | Clics | Tiempo (s) | Dificultades observadas |
|--|--|--|--|--|--|--|
| 1 | Dash | | | | | |
| 1 | Power BI | | | | | |
| 2 | Power BI | | | | | |
| 2 | Dash | | | | | |
| 3 | Dash | | | | | |
| 3 | Power BI | | | | | |

Entorno. Equipo, sistema operativo y navegador de Dash, versión de Power BI Desktop, quién ejecutó y su
experiencia previa con cada herramienta.

## 7. Indicadores para verificar la consistencia

Se comparan dos indicadores con los mismos filtros y la misma regla de agregación en las dos versiones.
Si no coinciden, se documenta la causa y, si es un error, se corrige en ambas versiones antes de
comparar, como pide el enunciado.

| Indicador | Filtros | Agregación | Valor del Lab 10 |
|--|--|--|--|
| I1. Llegadas por vía aérea en 2025 | Año 2025, vía Aérea, turistas y excursionistas | Suma de visitantes | 1,188,971 |
| I2. MAE del ARIMA(1,1,1) en la serie Total | Serie Total, conjunto de prueba completo, 63 meses | Promedio del error absoluto mensual | 154,494 |

Como control adicional se puede comparar la recuperación de 2025 frente a 2019, 3,352,289 entre
4,132,251, que da 81.1 %.

Estos valores ya se comprobaron en las tablas exportadas con `tests/test_export_powerbi.py`, así que una
diferencia en Power BI apuntaría a una relación o a una medida DAX y no a los datos. Las discrepancias
esperables son de redondeo, porque los visitantes de la base tienen decimales, y Power BI y
Dash pueden redondear distinto al mostrar.
