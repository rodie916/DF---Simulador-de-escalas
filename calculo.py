"""Lógica del simulador de cuotas de Pregrado (misma regla que el Excel 'Simulador de Cuotas Pregrado_VF')."""
from dataclasses import dataclass

ESCALAS = {"1": 1411, "2": 1093, "3": 829, "4": 609, "5": 444, "6": 328, "7": 223, "FB": 331}
CREDITOS_CUOTA_1 = 3.8
DERECHO_ENSENANZA = 380.0


def redondear(x: float) -> float:
    """Redondeo a 2 decimales como ROUND de Excel (0.5 se aleja de cero)."""
    return float(f"{x + 1e-9:.2f}") if x >= 0 else -float(f"{-x + 1e-9:.2f}")


@dataclass
class Resultado:
    valor_credito: float
    creditos_adm_por_cuota: float   # créditos administrativos que van en cada cuota 2-5
    creditos_extra_por_cuota: float  # créditos extra académicos que van en cada cuota 2-5
    cuotas: list
    total: float
    errores: list
    advertencias: list


def calcular(escala: str, creditos_adm: float, creditos_extra: float,
             derecho: float = DERECHO_ENSENANZA) -> Resultado:
    valor = ESCALAS[escala]
    errores, advertencias = [], []

    if creditos_adm < CREDITOS_CUOTA_1:
        errores.append("Los créditos administrativos deben ser al menos 3.8.")
    if creditos_extra < 0 or creditos_extra > creditos_adm:
        errores.append("Los créditos extra académicos no pueden ser negativos ni mayores al total de créditos administrativos.")
    elif not errores and creditos_adm - creditos_extra < CREDITOS_CUOTA_1:
        advertencias.append(
            "Los créditos administrativos sin los extra académicos son menores a 3.8. "
            "La cuota 1 igual cobra 3.8 créditos, así que el total puede no coincidir con "
            "créditos × valor + derecho. Valida este caso con Tesorería."
        )

    resto = max(creditos_adm - creditos_extra - CREDITOS_CUOTA_1, 0) / 4
    extra_q = creditos_extra / 4
    c1 = redondear(CREDITOS_CUOTA_1 * valor + derecho)
    cn = redondear(resto * valor + (creditos_extra * valor) / 4)
    cuotas = [c1, cn, cn, cn, cn]
    return Resultado(valor, resto, extra_q, cuotas, redondear(sum(cuotas)), errores, advertencias)
