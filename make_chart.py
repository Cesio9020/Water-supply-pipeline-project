import os
import matplotlib.pyplot as plt

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
    summary = result["summary"]

    # Create images folder
    os.makedirs("images", exist_ok=True)

    # Plot
    plt.figure(figsize=(8, 5))
    plt.bar(summary["Diâmetro"], summary["Custo Total (€)"])
    plt.xlabel("Diâmetro")
    plt.ylabel("Custo Total (€)")
    plt.title("Comparação do Custo Total por Diâmetro")

    plt.tight_layout()
    plt.savefig("images/cost_comparison.png", dpi=200)
    plt.close()


if __name__ == "__main__":
    main()