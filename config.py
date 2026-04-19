
from dataclasses import dataclass


@dataclass
class ProjectConfig:
    ano_base: int = 2003
    horizonte_anos: int = 40
    incremento_anos: int = 5

    taxa_atualizacao: float = 0.05
    preco_energia: float = 0.07
    perdas_rede: float = 0.10

    fator_p_diario_pop: float = 1.5
    fator_p_insta_pop: float = 3.0

    fator_p_diario_hotel: float = 1.5
    fator_p_insta_hotel: float = 3.0

    fator_p_diario_industria: float = 1.0

    hospedes_hotel: int = 200
    capitacao_hotel_l_hospede_dia: float = 500.0

    caudal_ind_16h_m3_h: float = 18.0
    caudal_ind_8h_m3_h: float = 36.0

    potencia_ano20_diametro250_kw: float = 45.1
    potencia_ano20_diametro315_kw: float = 42.62
    potencia_ano40_diametro250_kw: float = 56.81
    potencia_ano40_diametro315_kw: float = 52.65

    investimento_250: float = 0.0
    investimento_315: float = 0.0