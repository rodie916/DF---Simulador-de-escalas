# Simulador de cuotas – Pregrado (UP)

Herramienta referencial para orientar a estudiantes sobre el cálculo de sus 5 cuotas de Pregrado.
Replica la lógica del Excel *Simulador de Cuotas Pregrado_VF*.

## Regla de cálculo
- **Cuota 1:** 3.8 créditos administrativos × valor por crédito + derecho de enseñanza (S/ 380 por defecto).
- **Cuotas 2 a 5:** `(créditos adm. − extra académicos − 3.8) / 4` créditos + `extra académicos / 4` créditos, × valor por crédito.
- Cada cuota se redondea a 2 decimales.

Las escalas y el valor por crédito están en `calculo.py` (`ESCALAS`). Para actualizar las escalas de otro año, edita solo ese diccionario.

## Correr en local
```bash
python -m venv .venv
# Windows: .venv\Scripts\activate   |   Mac/Linux: source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Pruebas
```bash
pip install pytest
pytest
```

## Estructura
```
app.py               # interfaz Streamlit
calculo.py           # lógica (sin dependencias de Streamlit)
test_calculo.py      # pruebas con el ejemplo del Excel
.streamlit/config.toml  # tema con los colores institucionales
```

> Montos referenciales. Validar los importes definitivos según las disposiciones institucionales vigentes.
