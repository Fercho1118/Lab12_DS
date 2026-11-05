"""
Exporta los datos y resultados del Lab 10 como tablas para Power BI (modelo estrella).

No entrena modelos: las predicciones y métricas se copian tal cual de data/lab10/
(outputs/ del repo del Lab 10) y solo se les agregan identificadores para relacionarlas.

    python scripts/export_powerbi.py      # escribe powerbi/data/*.csv
"""
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "Base_Migracion_2009-2026jun.xlsx"
LAB10 = ROOT / "data" / "lab10"
OUT = ROOT / "powerbi" / "data"

MONTHS = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
VIAS = ["Aérea", "Terrestre", "Marítima"]
SERIES = ["Total", "Aérea", "Terrestre"]
MODELS = {  # orden, color y trazo iguales a los del tablero del Lab 10
    "ARIMA(1,1,1)": (1, "#6A3D9A", "Continua"),
    "Holt-Winters": (2, "#CC79A7", "Raya-punto"),
    "Seasonal Naive": (3, "#8C8C8C", "Punteada"),
}
EVAL_SET = "Prueba 70/30: abr-2021 a jun-2026 (63 meses no vistos)"


def load_arrivals(path=RAW) -> pd.DataFrame:
    """Turista + Excursionista, la misma definición del Lab 1 y del tablero del Lab 10."""
    df = pd.read_excel(path, sheet_name="Datos")
    df = df[df["Tipo de Viajero"].isin(["Turista", "Excursionista"])]
    df = df.assign(Fecha=pd.to_datetime(dict(year=df["Año"], month=df["Mes cod"], day=1)))
    # la hoja trae "Región" y "Región dos"; el Lab 10 usa "Región dos"
    cols = ["Fecha", "Vía", "Frontera", "País", "Región dos", "Agrupación Residencia",
            "Tipo de Viajero", "Viajero"]
    return df[cols].rename(columns={"Región dos": "Región", "Agrupación Residencia": "Mercado",
                                    "Tipo de Viajero": "Tipo"})


def fecha_id(fecha: pd.Series) -> pd.Series:
    return fecha.dt.year * 100 + fecha.dt.month


def dim_fecha(fechas: pd.Series) -> pd.DataFrame:
    f = pd.Series(pd.date_range(fechas.min(), fechas.max(), freq="MS"))
    months_per_year = f.dt.year.value_counts()
    return pd.DataFrame({
        "FechaId": fecha_id(f), "Fecha": f.dt.date, "Año": f.dt.year,
        "Trimestre": "T" + f.dt.quarter.astype(str), "Mes": f.dt.month,
        "MesNombre": f.dt.month.map(lambda m: MONTHS[m - 1]),
        "MesAño": f.dt.month.map(lambda m: MONTHS[m - 1]) + " " + f.dt.year.astype(str),
        # 2026 solo tiene ene-jun: el informe debe marcarlo como año parcial
        "AñoCompleto": f.dt.year.map(months_per_year).eq(12),
    })


def ids(values, name: str) -> pd.DataFrame:
    """Catálogo con identificador entero estable (orden alfabético)."""
    return pd.DataFrame({name: sorted(pd.unique(values))}).rename_axis(f"{name}Id").reset_index() \
        .assign(**{f"{name}Id": lambda d: d[f"{name}Id"] + 1})


def build_arrivals(raw: pd.DataFrame) -> dict[str, pd.DataFrame]:
    # Una misma frontera aparece con dos vías (p. ej. La Aurora registra algunas llegadas terrestres),
    # por eso la clave de la frontera es la pareja vía-frontera.
    fronteras = raw[["Vía", "Frontera"]].drop_duplicates().sort_values(["Vía", "Frontera"])
    fronteras = fronteras.assign(
        FronteraId=range(1, len(fronteras) + 1),
        Punto=fronteras["Frontera"].str.replace(r"^\d+\s*", "", regex=True),
        OrdenVía=fronteras["Vía"].map({v: i for i, v in enumerate(VIAS, 1)}),
    )[["FronteraId", "Vía", "OrdenVía", "Frontera", "Punto"]]

    # Región es atributo del país (1 a 1); el mercado de residencia no, cambia de agrupación con
    # los años, así que va como dimensión aparte y se conserva tal cual lo usa el Lab 10.
    paises = raw.groupby("País", as_index=False)["Región"].first()
    paises = paises.assign(Región=paises["Región"].replace("0", "Sin región"),
                           EsExtranjero=paises["País"].ne("Guatemala"))
    paises = paises.reset_index(names="PaisId").assign(PaisId=lambda d: d["PaisId"] + 1)
    mercados = ids(raw["Mercado"], "Mercado").assign(EsExtranjero=lambda d: d["Mercado"].ne("Guatemala"))

    fact = (raw.merge(fronteras[["FronteraId", "Vía", "Frontera"]], on=["Vía", "Frontera"])
            .merge(paises[["PaisId", "País"]], on="País")
            .merge(mercados[["MercadoId", "Mercado"]], on="Mercado")
            .assign(FechaId=lambda d: fecha_id(d["Fecha"])))
    fact = fact[["FechaId", "FronteraId", "PaisId", "MercadoId", "Tipo", "Viajero"]] \
        .sort_values(["FechaId", "FronteraId", "PaisId", "MercadoId", "Tipo"])
    return {"dim_fecha": dim_fecha(raw["Fecha"]), "dim_frontera": fronteras,
            "dim_pais": paises[["PaisId", "País", "Región", "EsExtranjero"]],
            "dim_mercado": mercados, "fact_llegadas": fact}


def build_models(preds: pd.DataFrame, met: pd.DataFrame) -> dict[str, pd.DataFrame]:
    preds = preds.assign(Fecha=pd.to_datetime(preds["Fecha"]))
    preds = preds.assign(FechaId=fecha_id(preds["Fecha"]),
                         SerieFechaId=preds["Serie"] + "|" + fecha_id(preds["Fecha"]).astype(str))
    modelos = pd.DataFrame([{"ModeloId": o, "Modelo": m, "Color": c, "Trazo": t}
                            for m, (o, c, t) in MODELS.items()])
    series = pd.DataFrame({"Serie": SERIES, "OrdenSerie": range(1, 4),
                           "Descripción": ["Todas las vías, incluida la marítima",
                                           "Solo vía aérea", "Solo vía terrestre"]})

    obs = preds[preds["Modelo"] == "Observado"]
    observada = obs[["SerieFechaId", "Serie", "FechaId", "Valor", "Tramo"]].rename(
        columns={"Valor": "Observado"})

    # El observado se copia en cada fila de predicción para calcular el error fila a fila,
    # sin cruzar tablas; la prueba de consistencia comprueba que la copia es idéntica.
    est = preds[preds["Modelo"] != "Observado"].merge(
        obs[["SerieFechaId", "Valor"]].rename(columns={"Valor": "Observado"}), on="SerieFechaId")
    est = est.merge(modelos[["ModeloId", "Modelo"]], on="Modelo").rename(columns={"Valor": "Estimado"})
    est = est.assign(Error=est["Observado"] - est["Estimado"])  # positivo = el modelo se quedó corto
    est = est.assign(ErrorAbs=est["Error"].abs())
    predicciones = est[["SerieFechaId", "Serie", "FechaId", "ModeloId", "Observado", "Estimado",
                        "Error", "ErrorAbs"]].sort_values(["Serie", "ModeloId", "FechaId"])

    test = observada[observada["Tramo"] == "test"]["FechaId"]
    metricas = met.merge(modelos[["ModeloId", "Modelo"]], on="Modelo").assign(
        Conjunto=EVAL_SET, MesesEvaluacion=test.nunique(),
        PrimerMes=test.min(), UltimoMes=test.max())
    metricas = metricas[["Serie", "ModeloId", "MAE", "RMSE", "MAPE", "Conjunto",
                         "MesesEvaluacion", "PrimerMes", "UltimoMes"]]
    return {"dim_serie": series, "dim_modelo": modelos, "fact_serie_observada": observada,
            "fact_predicciones": predicciones, "fact_metricas": metricas}


def export(raw_path=RAW, lab10=LAB10, out=OUT) -> dict[str, pd.DataFrame]:
    tables = build_arrivals(load_arrivals(raw_path))
    tables |= build_models(pd.read_csv(lab10 / "predictions.csv"), pd.read_csv(lab10 / "metrics.csv"))
    out.mkdir(parents=True, exist_ok=True)
    for name, df in tables.items():
        # UTF-8 con BOM para que Power Query detecte las tildes sin configurar el origen
        df.to_csv(out / f"{name}.csv", index=False, encoding="utf-8-sig", float_format="%.6f")
    return tables


if __name__ == "__main__":
    for name, df in export().items():
        print(f"{name:22s} {len(df):>7,} filas")
    print(f"\nTablas en {OUT.relative_to(ROOT)}/")
