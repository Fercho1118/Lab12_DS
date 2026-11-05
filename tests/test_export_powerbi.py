"""
Consistencia de las tablas de Power BI con el Lab 10: claves únicas, relaciones completas y
mismos totales y métricas que el tablero de Dash. Requiere haber corrido scripts/export_powerbi.py.
"""
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "powerbi" / "data"
LAB10 = ROOT / "data" / "lab10"


def read(name: str) -> pd.DataFrame:
    return pd.read_csv(DATA / f"{name}.csv", encoding="utf-8-sig")


T = {n: read(n) for n in ["dim_fecha", "dim_frontera", "dim_pais", "dim_mercado", "dim_serie",
                          "dim_modelo", "fact_llegadas", "fact_serie_observada",
                          "fact_predicciones", "fact_metricas"]}

# Valores del tablero del Lab 10 (commit 27d624b de nicoCT04/Lab10-DataSicence)
LAB10_2025_TOTAL = 3_352_288.657508455
LAB10_2025_AEREA = 1_188_971.0
LAB10_2019_TOTAL = 4_132_250.601876994
LAB10_2025_CENTRO = 0.6394716441843693  # peso de América Del Centro en extranjeros 2025 (V5)


def arrivals() -> pd.DataFrame:
    return (T["fact_llegadas"].merge(T["dim_fecha"], on="FechaId").merge(T["dim_frontera"], on="FronteraId")
            .merge(T["dim_pais"], on="PaisId"))


class Keys(unittest.TestCase):
    def test_dimension_keys_are_unique(self):
        for dim, key in [("dim_fecha", "FechaId"), ("dim_frontera", "FronteraId"), ("dim_pais", "PaisId"),
                         ("dim_mercado", "MercadoId"), ("dim_serie", "Serie"), ("dim_modelo", "ModeloId")]:
            self.assertTrue(T[dim][key].is_unique, dim)

    def test_fact_grain_has_no_duplicates(self):
        grains = {"fact_llegadas": ["FechaId", "FronteraId", "PaisId", "MercadoId", "Tipo"],
                  "fact_serie_observada": ["SerieFechaId"],
                  "fact_predicciones": ["SerieFechaId", "ModeloId"],
                  "fact_metricas": ["Serie", "ModeloId"]}
        for fact, grain in grains.items():
            self.assertFalse(T[fact].duplicated(grain).any(), fact)

    def test_every_foreign_key_exists_in_its_dimension(self):
        links = [("fact_llegadas", "FechaId", "dim_fecha"), ("fact_llegadas", "FronteraId", "dim_frontera"),
                 ("fact_llegadas", "PaisId", "dim_pais"), ("fact_llegadas", "MercadoId", "dim_mercado"),
                 ("fact_serie_observada", "FechaId", "dim_fecha"), ("fact_serie_observada", "Serie", "dim_serie"),
                 ("fact_predicciones", "FechaId", "dim_fecha"), ("fact_predicciones", "ModeloId", "dim_modelo"),
                 ("fact_predicciones", "Serie", "dim_serie"), ("fact_metricas", "ModeloId", "dim_modelo"),
                 ("fact_metricas", "Serie", "dim_serie")]
        for fact, key, dim in links:
            self.assertTrue(T[fact][key].isin(T[dim][key]).all(), f"{fact}.{key}")

    def test_partial_year_is_flagged(self):
        d = T["dim_fecha"]
        self.assertFalse(d.loc[d["Año"] == 2026, "AñoCompleto"].any())
        self.assertTrue(d.loc[d["Año"] == 2025, "AñoCompleto"].all())


class SameResultsAsLab10(unittest.TestCase):
    def test_yearly_totals_match_dashboard(self):
        a = arrivals()
        self.assertAlmostEqual(a.loc[a["Año"] == 2025, "Viajero"].sum(), LAB10_2025_TOTAL, places=2)
        self.assertAlmostEqual(a.loc[a["Año"] == 2019, "Viajero"].sum(), LAB10_2019_TOTAL, places=2)
        self.assertAlmostEqual(a.loc[(a["Año"] == 2025) & (a["Vía"] == "Aérea"), "Viajero"].sum(),
                               LAB10_2025_AEREA, places=2)

    def test_region_share_matches_treemap(self):
        a = arrivals()
        x = a[(a["Año"] == 2025) & a["EsExtranjero"]]
        share = x.loc[x["Región"] == "América Del Centro", "Viajero"].sum() / x["Viajero"].sum()
        self.assertAlmostEqual(share, LAB10_2025_CENTRO, places=6)

    def test_observed_series_equal_sum_of_arrivals(self):
        a = arrivals()
        sums = {"Total": a.groupby("FechaId")["Viajero"].sum()}
        for via in ["Aérea", "Terrestre"]:
            sums[via] = a[a["Vía"] == via].groupby("FechaId")["Viajero"].sum()
        obs = T["fact_serie_observada"]
        for serie, s in sums.items():
            o = obs[obs["Serie"] == serie].set_index("FechaId")["Observado"]
            np.testing.assert_allclose(o.sort_index().values, s.reindex(o.index).sort_index().values,
                                       rtol=1e-9, err_msg=serie)

    def test_predictions_are_copied_unchanged(self):
        src = pd.read_csv(LAB10 / "predictions.csv")
        src = src[src["Modelo"] != "Observado"]
        p = T["fact_predicciones"].merge(T["dim_modelo"], on="ModeloId")
        self.assertEqual(len(p), len(src))
        self.assertAlmostEqual(p["Estimado"].sum(), src["Valor"].sum(), delta=1e-3)

    def test_copied_observed_value_is_identical(self):
        p = T["fact_predicciones"].merge(T["fact_serie_observada"], on="SerieFechaId", suffixes=("", "_obs"))
        self.assertEqual(len(p), len(T["fact_predicciones"]))
        self.assertTrue(p["Tramo"].eq("test").all())
        np.testing.assert_allclose(p["Observado"], p["Observado_obs"], rtol=0, atol=1e-6)

    def test_metrics_recomputed_from_predictions_match_lab10(self):
        p = T["fact_predicciones"]
        met = T["fact_metricas"]
        for (serie, model), g in p.groupby(["Serie", "ModeloId"]):
            row = met[(met["Serie"] == serie) & (met["ModeloId"] == model)].iloc[0]
            self.assertAlmostEqual(g["ErrorAbs"].mean(), row["MAE"], delta=1e-3)
            self.assertAlmostEqual(np.sqrt((g["Error"] ** 2).mean()), row["RMSE"], delta=1e-3)
            self.assertAlmostEqual((g["ErrorAbs"] / g["Observado"]).mean() * 100, row["MAPE"], delta=1e-4)
            self.assertEqual(row["MesesEvaluacion"], len(g))

    def test_metrics_table_is_unchanged(self):
        src = pd.read_csv(LAB10 / "metrics.csv")
        m = T["fact_metricas"].merge(T["dim_modelo"], on="ModeloId").merge(src, on=["Serie", "Modelo"],
                                                                           suffixes=("", "_lab10"))
        self.assertEqual(len(m), 9)
        for col in ["MAE", "RMSE", "MAPE"]:
            np.testing.assert_allclose(m[col], m[f"{col}_lab10"], atol=1e-5)


if __name__ == "__main__":
    unittest.main()
