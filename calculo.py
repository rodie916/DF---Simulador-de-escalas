"""Lógica del simulador de cuotas de Pregrado.

Misma regla que el Excel 'Simulador de Cuotas Pregrado_VF':
- Cuota 1 = 3.8 créditos × valor del crédito + derecho de matrícula.
- Cuotas 2 a 5 = (créditos de cursos − 3.8) / 4 + (créditos de talleres) / 4, × valor del crédito.
  (créditos de cursos = créditos administrativos sin los talleres / extra académicos)

Este módulo no depende de Streamlit: el mismo cálculo puede usarse desde cualquier web.
"""
from dataclasses import dataclass, field

# Configuración del periodo. La escala NO se elige: viene del sistema al iniciar sesión.
PERIODO = "2026-II"
ESCALAS = {"1": 1411, "2": 1093, "3": 829, "4": 609, "5": 444, "6": 328, "7": 223, "FB": 331}
CREDITOS_CUOTA_1 = 3.8
DERECHO_MATRICULA = 380.0
PASO_CREDITOS = 0.5
NUM_CUOTAS = 5


def redondear(x: float) -> float:
    """Redondeo a 2 decimales como ROUND de Excel (0.5 se aleja de cero)."""
    return float(f"{x + 1e-9:.2f}")


@dataclass
class Cuota:
    numero: int
    monto: float
    creditos_cursos: float
    creditos_talleres: float
    incluye_matricula: bool
    glosa: str


@dataclass
class Resultado:
    escala: str
    valor_credito: float
    creditos_cursos: float
    creditos_talleres: float
    derecho_matricula: float
    cuotas: list = field(default_factory=list)
    total: float = 0.0
    errores: list = field(default_factory=list)
    advertencias: list = field(default_factory=list)

    @property
    def creditos_totales(self) -> float:
        return self.creditos_cursos + self.creditos_talleres


def _es_multiplo(x: float, paso: float = PASO_CREDITOS) -> bool:
    return abs(round(x / paso) * paso - x) < 1e-9


def calcular(escala: str, creditos_cursos: float, creditos_talleres: float = 0.0,
             derecho_matricula: float = DERECHO_MATRICULA) -> Resultado:
    """creditos_cursos: créditos de los cursos (sin talleres). creditos_talleres: créditos extra académicos."""
    valor = ESCALAS[escala]
    r = Resultado(escala, valor, creditos_cursos, creditos_talleres, derecho_matricula)

    if creditos_cursos < 0 or creditos_talleres < 0:
        r.errores.append("Los créditos no pueden ser negativos.")
    if not (_es_multiplo(creditos_cursos) and _es_multiplo(creditos_talleres)):
        r.errores.append("Los créditos deben ingresarse de 0.5 en 0.5.")
    if creditos_cursos + creditos_talleres < CREDITOS_CUOTA_1:
        r.errores.append("Debes tener al menos 4 créditos en total para simular.")
    elif creditos_cursos < CREDITOS_CUOTA_1:
        r.advertencias.append(
            "Tus créditos de cursos (sin talleres) son menos de 3.8. La cuota 1 igual considera 3.8 créditos, "
            "así que el total puede ser mayor que créditos × valor del crédito + derecho de matrícula. "
            "Consulta este caso con Tesorería."
        )
    if r.errores:
        return r

    cursos_q = max(creditos_cursos - CREDITOS_CUOTA_1, 0) / 4
    talleres_q = creditos_talleres / 4
    c1 = redondear(CREDITOS_CUOTA_1 * valor + derecho_matricula)
    cn = redondear(cursos_q * valor + (creditos_talleres * valor) / 4)

    r.cuotas.append(Cuota(1, c1, CREDITOS_CUOTA_1, 0.0, True,
                          f"{fmt(CREDITOS_CUOTA_1)} créditos × {soles(valor)} + {soles(derecho_matricula)} de derecho de matrícula"))
    for n in range(2, NUM_CUOTAS + 1):
        partes = [f"{fmt(cursos_q)} créditos de cursos"]
        if creditos_talleres:
            partes.append(f"{fmt(talleres_q)} créditos de talleres")
        r.cuotas.append(Cuota(n, cn, cursos_q, talleres_q, False,
                              f"{' + '.join(partes)} = {fmt(cursos_q + talleres_q)} créditos × {soles(valor)}"))
    r.total = redondear(sum(c.monto for c in r.cuotas))
    return r


def explicacion(r: Resultado) -> list:
    """Pasos en lenguaje simple para que el alumno entienda de dónde sale cada monto."""
    if r.errores:
        return []
    cursos_rest = max(r.creditos_cursos - CREDITOS_CUOTA_1, 0)
    pasos = [
        ("Tu valor por crédito",
         f"Según tu escala, cada crédito cuesta {soles(r.valor_credito)}."),
        ("Cuota 1: monto fijo",
         f"La primera cuota siempre considera {fmt(CREDITOS_CUOTA_1)} créditos ({fmt(CREDITOS_CUOTA_1)} × {soles(r.valor_credito)} = "
         f"{soles(redondear(CREDITOS_CUOTA_1 * r.valor_credito))}) más el derecho de matrícula de {soles(r.derecho_matricula)}. "
         f"Total cuota 1: {soles(r.cuotas[0].monto)}."),
        ("Cuotas 2 a 5: tus créditos restantes",
         f"De tus {fmt(r.creditos_cursos)} créditos de cursos ya se cobraron {fmt(CREDITOS_CUOTA_1)} en la cuota 1. "
         f"Los {fmt(cursos_rest)} restantes se dividen en 4 partes iguales: {fmt(cursos_rest / 4)} créditos por cuota."),
    ]
    if r.creditos_talleres:
        pasos.append(("Talleres (extra académicos)",
                      f"Los créditos de talleres ({fmt(r.creditos_talleres)}) no van en la cuota 1: se dividen entre las cuotas 2 a 5, "
                      f"{fmt(r.creditos_talleres / 4)} créditos por cuota."))
    pasos.append(("Total del periodo",
                  f"Cuota 1 ({soles(r.cuotas[0].monto)}) + 4 cuotas de {soles(r.cuotas[1].monto)} = {soles(r.total)}. "
                  "Cada cuota se redondea a 2 decimales."))
    return pasos


def resumen_texto(r: Resultado, periodo: str = PERIODO) -> str:
    if r.errores:
        return ""
    lineas = [f"Simulación de cuotas – Pregrado {periodo}",
              f"Escala {r.escala} · {fmt(r.creditos_cursos)} créditos de cursos"
              + (f" + {fmt(r.creditos_talleres)} de talleres" if r.creditos_talleres else "")]
    lineas += [f"Cuota {c.numero}: {soles(c.monto)}" for c in r.cuotas]
    lineas += [f"Total del periodo: {soles(r.total)}", "Montos referenciales, sujetos a validación."]
    return "\n".join(lineas)


def soles(x: float) -> str:
    return f"S/ {x:,.2f}"


def fmt(x: float) -> str:
    """Créditos: sin decimales si es entero, si no con los necesarios (máx. 3)."""
    s = f"{x:.3f}".rstrip("0").rstrip(".")
    return s
