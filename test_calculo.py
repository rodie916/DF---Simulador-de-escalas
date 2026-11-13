from calculo import calcular, explicacion, resumen_texto
from datos_alumno import ALUMNOS_DEMO
from pdf_resumen import generar_pdf


def test_ejemplo_excel():
    # Excel: escala 5, 21 créditos administrativos de los cuales 1 es extra académico
    r = calcular("5", 20, 1)
    assert [c.monto for c in r.cuotas] == [2067.20, 1909.20, 1909.20, 1909.20, 1909.20]
    assert r.total == 9704.00
    assert not r.errores and not r.advertencias


def test_sin_talleres():
    r = calcular("1", 22, 0)
    assert r.cuotas[0].monto == round(3.8 * 1411 + 380, 2)
    assert r.total == round(22 * 1411 + 380, 2)


def test_pasos_de_medio_credito():
    assert not calcular("2", 20.5, 0.5).errores
    assert calcular("2", 20.3, 0).errores


def test_minimo_creditos():
    assert calcular("1", 3, 0).errores


def test_caso_borde_advierte():
    r = calcular("5", 3, 1)
    assert r.advertencias and not r.errores


def test_explicacion_y_resumen():
    r = calcular("3", 18, 1)
    assert len(explicacion(r)) == 5
    assert "Total del periodo" in resumen_texto(r)


def test_alumno_matriculado_suma_creditos():
    a = ALUMNOS_DEMO["Alumno con matrícula registrada"]
    assert (a.creditos_cursos, a.creditos_talleres) == (20, 1)


def test_pdf_se_genera():
    pdf = generar_pdf(calcular("2", 20, 1), "2026-II")
    assert pdf[:4] == b"%PDF" and len(pdf) > 1000
