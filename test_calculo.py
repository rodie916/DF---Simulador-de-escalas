from calculo import calcular


def test_ejemplo_excel():
    r = calcular("5", 21, 1)
    assert r.cuotas == [2067.20, 1909.20, 1909.20, 1909.20, 1909.20]
    assert r.total == 9704.00
    assert not r.errores and not r.advertencias


def test_minimo_creditos():
    assert calcular("1", 3.0, 0).errores


def test_extra_mayor_que_total():
    assert calcular("3", 10, 12).errores


def test_caso_borde_advierte():
    r = calcular("5", 4, 1)
    assert r.advertencias and not r.errores
