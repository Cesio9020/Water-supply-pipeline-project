import pandas as pd

from config import ProjectConfig
from pipeline import run_pipeline


def make_config() -> ProjectConfig:
    return ProjectConfig(
        taxa_atualizacao=0.05,
        preco_energia=0.07,
        investimento_250=120000,
        investimento_315=145000,
    )


def test_pipeline_runs_and_returns_expected_keys():
    cfg = make_config()
    result = run_pipeline(cfg)

    expected_keys = {
        "census",
        "regression_table",
        "ta",
        "intercepto",
        "r_squared",
        "population_forecast",
        "hotel_demand",
        "industry_demand",
        "total_demand",
        "summary",
    }

    assert isinstance(result, dict)
    assert expected_keys.issubset(result.keys())


def test_regression_outputs_are_reasonable():
    cfg = make_config()
    result = run_pipeline(cfg)

    ta = result["ta"]
    r_squared = result["r_squared"]

    assert ta > 0
    assert 0 <= r_squared <= 1


def test_summary_table_has_expected_columns():
    cfg = make_config()
    result = run_pipeline(cfg)

    summary = result["summary"]

    assert isinstance(summary, pd.DataFrame)
    assert not summary.empty
    assert list(summary.columns) == [
        "Diâmetro",
        "Investimento Inicial (€)",
        "Energia Descontada (€)",
        "Custo Total (€)",
    ]
    assert len(summary) == 2


def test_total_cost_equals_investment_plus_discounted_energy():
    cfg = make_config()
    result = run_pipeline(cfg)

    summary = result["summary"]

    for _, row in summary.iterrows():
        expected_total = row["Investimento Inicial (€)"] + row["Energia Descontada (€)"]
        assert row["Custo Total (€)"] == expected_total


def test_discounted_cost_is_not_greater_than_nominal_cost():
    cfg = make_config()
    result = run_pipeline(cfg)

    df = result["total_demand"]

    nominal_250 = df[("Custos de Energia€", "diametro 250mm")]
    discounted_250 = df[("Custos Descontados €", "diametro 250mm")]

    nominal_315 = df[("Custos de Energia€", "diametro 315mm")]
    discounted_315 = df[("Custos Descontados €", "diametro 315mm")]

    assert (discounted_250 <= nominal_250).all()
    assert (discounted_315 <= nominal_315).all()


def test_population_forecast_is_non_decreasing():
    cfg = make_config()
    result = run_pipeline(cfg)

    pop = result["population_forecast"]["Previsão da Pp"]

    assert pop.is_monotonic_increasing


def test_total_demands_are_positive():
    cfg = make_config()
    result = run_pipeline(cfg)

    df = result["total_demand"]

    qmd = df[("", "Qmd(m³/dia)")]
    qpd = df[("", "Qpd(m³/dia)")]
    tempo = df[("", "Tempo medio da bomba(h/dia)")]

    assert (qmd > 0).all()
    assert (qpd > 0).all()
    assert (tempo > 0).all()


def test_qpd_is_greater_than_or_equal_to_qmd():
    cfg = make_config()
    result = run_pipeline(cfg)

    df = result["total_demand"]

    qmd = df[("", "Qmd(m³/dia)")]
    qpd = df[("", "Qpd(m³/dia)")]

    assert (qpd >= qmd).all()


def test_diameter_315_has_lower_or_equal_energy_cost_than_250():
    cfg = make_config()
    result = run_pipeline(cfg)

    df = result["total_demand"]

    custo_250 = df[("Custos de Energia€", "diametro 250mm")]
    custo_315 = df[("Custos de Energia€", "diametro 315mm")]

    assert (custo_315 <= custo_250).all()