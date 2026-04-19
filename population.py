import pandas as pd
import numpy as np
from config import ProjectConfig


def build_census_table() -> pd.DataFrame:
    return pd.DataFrame({
        "Ano do Censo": [1900, 1911, 1920, 1930, 1940, 1950, 1960, 1970, 1981, 1991],
        "População registada (hab)": [4485, 4752, 5231, 5567, 6084, 6553, 6875, 6753, 6937, 7414],
    })


def fit_arithmetic_method(census: pd.DataFrame) -> dict:
    df = census.copy()
    df["Tempo inicial (ti)"] = df["Ano do Censo"] - 1900

    tm = df["Tempo inicial (ti)"].mean()
    pm = df["População registada (hab)"].mean()

    df["(ti-tm)"] = df["Tempo inicial (ti)"] - tm
    df["(pi-pm)"] = df["População registada (hab)"] - pm
    df["(ti-tm)^2"] = df["(ti-tm)"] ** 2
    df["(pi-pm)^2"] = df["(pi-pm)"] ** 2
    df["(ti-tm)*(pi-pm)"] = df["(ti-tm)"] * df["(pi-pm)"]

    sxx = df["(ti-tm)^2"].sum()
    syy = df["(pi-pm)^2"].sum()
    sxy = df["(ti-tm)*(pi-pm)"].sum()

    ta = sxy / sxx
    intercepto = pm - ta * tm
    r_squared = (sxy ** 2) / (sxx * syy)

    return {
        "table": df,
        "ta": ta,
        "intercepto": intercepto,
        "r_squared": r_squared,
    }


def forecast_population(cfg: ProjectConfig, intercepto: float, ta: float) -> pd.DataFrame:
    anos = list(range(cfg.ano_base, cfg.ano_base + cfg.horizonte_anos + 1, cfg.incremento_anos))

    df = pd.DataFrame({"Ano de previsão": anos})
    df["Parametro (A)"] = range(0, cfg.horizonte_anos + 1, cfg.incremento_anos)
    df["Tempo desde 1900"] = df["Ano de previsão"] - 1900
    df["Previsão da Pp"] = (intercepto + ta * df["Tempo desde 1900"]).round()

    A = df["Parametro (A)"]
    P = df["Previsão da Pp"]

    df["Capitação l/(hab.dia)"] = np.exp(
        1.0914 * (np.log(100 + 1.25 * A) - np.log(80 + A)) * np.log(P)
        + 9.2953 * np.log(80 + A)
        - 8.2953 * np.log(100 + 1.25 * A)
    ).round()

    df["Qmd m³/dia"] = (df["Capitação l/(hab.dia)"] * 1e-3 * P).round()
    df["Qpd m³/dia"] = df["Qmd m³/dia"] * cfg.fator_p_diario_pop
    df["Qpi (m³/hora)"] = (df["Qmd m³/dia"] / 24 * cfg.fator_p_insta_pop).round(2)
    df["Qpi litros/s"] = (df["Qpi (m³/hora)"] * 0.278).round(2)

    return df