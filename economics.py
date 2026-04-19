import pandas as pd
from config import ProjectConfig


def add_energy_costs(df: pd.DataFrame, cfg: ProjectConfig) -> pd.DataFrame:
    out = df.copy()

    out["diametro 250mm"] = 0.0
    out["diametro 315mm"] = 0.0

    new_cols = []
    for col in out.columns:
        if col in ["diametro 250mm", "diametro 315mm"]:
            new_cols.append(("Custos de Energia€", col))
        else:
            new_cols.append(("", col))
    out.columns = pd.MultiIndex.from_tuples(new_cols)

    tempo = out.loc[:, ("", "Tempo medio da bomba(h/dia)")]

    out.loc[:4, ("Custos de Energia€", "diametro 250mm")] = (
        cfg.potencia_ano20_diametro250_kw * tempo.loc[:4] * 365 * cfg.preco_energia
    ).round(2)
    out.loc[5:, ("Custos de Energia€", "diametro 250mm")] = (
        cfg.potencia_ano40_diametro250_kw * tempo.loc[5:] * 365 * cfg.preco_energia
    ).round(2)

    out.loc[:4, ("Custos de Energia€", "diametro 315mm")] = (
        cfg.potencia_ano20_diametro315_kw * tempo.loc[:4] * 365 * cfg.preco_energia
    ).round(2)
    out.loc[5:, ("Custos de Energia€", "diametro 315mm")] = (
        cfg.potencia_ano40_diametro315_kw * tempo.loc[5:] * 365 * cfg.preco_energia
    ).round(2)

    return out


def add_discounted_costs(df: pd.DataFrame, cfg: ProjectConfig) -> pd.DataFrame:
    out = df.copy()
    t = out.loc[:, ("", "Anos")]

    for d in ["diametro 250mm", "diametro 315mm"]:
        out.loc[:, ("Custos Descontados €", d)] = (
            out.loc[:, ("Custos de Energia€", d)] / (1 + cfg.taxa_atualizacao) ** t
        ).round(2)

    return out


def build_summary(df: pd.DataFrame, cfg: ProjectConfig) -> pd.DataFrame:
    vp_energia_250 = df.loc[:, ("Custos Descontados €", "diametro 250mm")].sum()
    vp_energia_315 = df.loc[:, ("Custos Descontados €", "diametro 315mm")].sum()

    total_250 = cfg.investimento_250 + vp_energia_250
    total_315 = cfg.investimento_315 + vp_energia_315

    return pd.DataFrame({
        "Diâmetro": ["250mm", "315mm"],
        "Investimento Inicial (€)": [cfg.investimento_250, cfg.investimento_315],
        "Energia Descontada (€)": [round(vp_energia_250, 2), round(vp_energia_315, 2)],
        "Custo Total (€)": [round(total_250, 2), round(total_315, 2)],
    })