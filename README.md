# Simulador de cuotas – Pregrado (UP)

Demo del simulador de cuotas de Pregrado (Tesorería – Dirección Financiera). Explica al alumno cuánto pagará
en cada cuota y **cómo se calcula** cada monto. En producción irá dentro de la web de pagos virtuales,
donde la escala y los cursos del alumno llegan del sistema al iniciar sesión.

## Regla de cálculo (igual al Excel *Simulador de Cuotas Pregrado_VF*)
- **Cuota 1:** 3.8 créditos × valor del crédito + derecho de matrícula (S/ 380, fijo).
- **Cuotas 2 a 5:** [(créditos de cursos − 3.8) / 4 + créditos de talleres / 4] × valor del crédito.
- Cada cuota se redondea a 2 decimales. Créditos de 0.5 en 0.5.

## Estructura
```
app.py            # interfaz Streamlit (demo, con alumnos de ejemplo en la barra lateral)
calculo.py        # lógica y textos explicativos (sin Streamlit) · periodo, escalas y matrícula aquí
datos_alumno.py   # formato de los datos del alumno + alumnos ficticios para la demo
pdf_resumen.py    # resumen imprimible en PDF
test_calculo.py   # pruebas
.streamlit/config.toml
```

## Correr en local
```bash
pip install -r requirements.txt
streamlit run app.py
pytest
```

> Montos referenciales. Los importes definitivos son los que figuran en la boleta.
