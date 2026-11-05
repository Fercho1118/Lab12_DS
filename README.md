# Lab 12 — Observatorio de turismo en Power BI

Segunda versión del tablero del observatorio de turismo sostenible (Laboratorio 10), ahora como
informe de Power BI Desktop. Usa los mismos datos, las mismas preguntas de gestión y los resultados
de los mismos tres modelos (ARIMA(1,1,1), Holt-Winters y Seasonal Naive). No se entrenan modelos.

Versión del Laboratorio 10 (Plotly Dash): <https://github.com/nicoCT04/Lab10-DataSicence>
(commit `27d624b`).

## Estructura

```
data/raw/Base_Migracion_2009-2026jun.xlsx   base de llegadas INGUAT/Migración (la misma del Lab 10)
data/lab10/predictions.csv, metrics.csv     resultados de los modelos, copiados sin cambios de outputs/ del Lab 10
scripts/export_powerbi.py                   genera las tablas de Power BI
powerbi/data/*.csv                          tablas que importa el informe (modelo estrella)
powerbi/observatorio_v1.pbix                informe de Power BI, versión 1 (avance)
tests/test_export_powerbi.py                consistencia con el Lab 10
docs/lab12/                                 diseño, planificación, protocolo de pruebas y modelo de Power BI (powerbi_avance.md)
```

## Generar las tablas

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
python scripts/export_powerbi.py
python -m unittest tests.test_export_powerbi -v
```

## Tablas para Power BI

| Tabla | Grano | Uso |
|--|--|--|
| `fact_llegadas` | mes × vía-frontera × país × mercado × tipo | Llegadas observadas (V1–V3, V5–V8) |
| `dim_fecha` | mes | Jerarquía Año › Trimestre › Mes, marca de año parcial (2026) |
| `dim_frontera` | vía-frontera | Vía y punto de ingreso; jerarquía Vía › Punto |
| `dim_pais` | país | Región › País; `EsExtranjero` excluye a guatemaltecos residentes fuera |
| `dim_mercado` | mercado de residencia | Ranking de mercados (V3), igual agrupación que el Lab 10 |
| `fact_serie_observada` | serie × mes | Observado de las series Total, Aérea y Terrestre, con tramo train/test |
| `fact_predicciones` | serie × mes × modelo | **Predicciones** de los tres modelos con su error (V4, V9) |
| `fact_metricas` | serie × modelo | **Métricas** MAE, RMSE y MAPE del conjunto de prueba |
| `dim_serie`, `dim_modelo` | | Selector de serie; color y trazo de cada modelo |
