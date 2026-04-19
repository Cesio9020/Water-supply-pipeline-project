import pandas as pd
from config import ProjectConfig


def hotel_demand(cfg: ProjectConfig) -> pd.DataFrame:
    capitacao_m3_hospede_dia = cfg.capitacao_hotel_l_hospede_dia / 1000

    df = pd.DataFrame({
        "Qmd (m³/dia)": [capitacao_m3_hospede_dia * cfg.hospedes_hotel]
    })

    df["Qpd (m³/dia)"] = df["Qmd (m³/dia)"] * cfg.fator_p_diario_hotel
    df["Qpi (m³/hora)"] = (df["Qmd (m³/dia)"] / 24) * cfg.fator_p_insta_hotel
    df["Qpi (litros/s)"] = df["Qpi (m³/hora)"] * 0.278

    return df


def industry_demand(cfg: ProjectConfig) -> pd.DataFrame:
    qmd = (16 * cfg.caudal_ind_16h_m3_h) + (8 * cfg.caudal_ind_8h_m3_h)
    qmh = qmd / 24
    fator_p_insta = cfg.caudal_ind_8h_m3_h / qmh

    df = pd.DataFrame({
        "Qmd (m³/dia)": [qmd],
        "Qpd (m³/dia)": [qmd * cfg.fator_p_diario_industria],
        "Qpi (m³/hora)": [qmh * fator_p_insta]
    })

    return df
    