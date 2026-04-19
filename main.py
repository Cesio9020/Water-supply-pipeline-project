from config import ProjectConfig
from pipeline import run_pipeline


def main():
    cfg = ProjectConfig(
        taxa_atualizacao=0.05,
        preco_energia=0.07,
        investimento_250=120000,
        investimento_315=145000,
    )

    result = run_pipeline(cfg)

    print("Taxa de crescimento (ta):", round(result["ta"], 4))
    print("R²:", round(result["r_squared"], 4))
    print()
    print(result["summary"])


if __name__ == "__main__":
    main()