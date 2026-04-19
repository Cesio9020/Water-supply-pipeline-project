from config import ProjectConfig
from population import build_census_table, fit_arithmetic_method, forecast_population
from demand import hotel_demand, industry_demand
from hydraulics import total_demand, pump_operating_time
from economics import add_energy_costs, add_discounted_costs, build_summary


def run_pipeline(cfg: ProjectConfig | None = None) -> dict:
    cfg = cfg or ProjectConfig()

    census = build_census_table()
    regression = fit_arithmetic_method(census)

    pop = forecast_population(cfg, regression["intercepto"], regression["ta"])
    hotel = hotel_demand(cfg)
    industry = industry_demand(cfg)

    totals = total_demand(pop, hotel, industry, cfg)
    totals = pump_operating_time(totals)
    totals = add_energy_costs(totals, cfg)
    totals = add_discounted_costs(totals, cfg)

    summary = build_summary(totals, cfg)

    return {
        "census": census,
        "regression_table": regression["table"],
        "ta": regression["ta"],
        "intercepto": regression["intercepto"],
        "r_squared": regression["r_squared"],
        "population_forecast": pop,
        "hotel_demand": hotel,
        "industry_demand": industry,
        "total_demand": totals,
        "summary": summary,
    }