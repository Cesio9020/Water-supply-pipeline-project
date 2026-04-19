import pandas as pd
import numpy as np
from config import ProjectConfig


def total_demand(
    pop_df: pd.DataFrame,
    hotel_df: pd.DataFrame,
    industry_df: pd.DataFrame,
    cfg: ProjectConfig,
) -> pd.DataFrame:
    df = pd.DataFrame()

    df["Ano de previsão"] = pop_df["Ano de previsão"]
    df["Anos"] = pop_df["Parametro (A)"]
    df["População(hab)"] = pop_df["Previsão da Pp"]

    df["Qmd(m³/dia)"] = (
        pop_df["Qmd m³/dia"]
        + hotel_df["Qmd (m³/dia)"].iloc[0]
        + industry_df["Qmd (m³/dia)"].iloc[0]
    ) * (1 + cfg.perdas_rede)

    df["Qpd(m³/dia)"] = (
        pop_df["Qpd m³/dia"]
        + hotel_df["Qpd (m³/dia)"].iloc[0]
        + industry_df["Qpd (m³/dia)"].iloc[0]
    ) * (1 + cfg.perdas_rede)

    return df


def pump_operating_time(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()

    qpd_ano20 = out.loc[4, "Qpd(m³/dia)"]
    out.loc[:4, "Tempo medio da bomba(h/dia)"] = np.trunc(
        (out.loc[:4, "Qmd(m³/dia)"] / qpd_ano20) * 16
    ).astype(int)

    qpd_ano40 = out.loc[8, "Qpd(m³/dia)"]
    out.loc[5:, "Tempo medio da bomba(h/dia)"] = np.ceil(
        (out.loc[5:, "Qmd(m³/dia)"] / qpd_ano40) * 16
    ).astype(int)

    return out