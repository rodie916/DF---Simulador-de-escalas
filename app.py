"""Simulador de cuotas – Pregrado (demo).

En producción este simulador va dentro de la web de pagos virtuales: el alumno ya inició sesión,
así que su escala y sus cursos llegan del sistema. Aquí se simulan con alumnos de ejemplo.
"""
import streamlit as st

from calculo import (DERECHO_MATRICULA, ESCALAS, PASO_CREDITOS, PERIODO,
                     calcular, explicacion, fmt, resumen_texto, soles)
from datos_alumno import ALUMNOS_DEMO
from pdf_resumen import generar_pdf

st.set_page_config(page_title="Simulador de cuotas – Pregrado", page_icon="🧮", layout="wide",
                   initial_sidebar_state="collapsed")

NAVY, GREEN, BLUE, CYAN, MAGENTA = "#0E1F43", "#00FF24", "#0062FF", "#61F2F2", "#D733FF"

st.markdown(f"""
<style>
@import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@600;700;800&family=Open+Sans:wght@400;600;700&display=swap');
html, body, [class*="css"], .stMarkdown, label {{ font-family: 'Open Sans', Arial, sans-serif; }}
.block-container {{ padding-top: 3.2rem; max-width: 1100px; }}
.hero {{ background:{NAVY}; color:#fff; border-radius:10px; padding:26px 28px 24px; position:relative; overflow:hidden; margin-bottom:18px; }}
.hero .brand {{ font-family:Montserrat,Arial,sans-serif; font-weight:800; font-size:13px; letter-spacing:.08em; text-transform:uppercase; line-height:1.15; }}
.hero h1 {{ font-family:Montserrat,Arial,sans-serif; color:{GREEN}; font-weight:800; font-size:34px; text-transform:uppercase; margin:18px 0 4px; padding:0; }}
.hero .sub {{ font-family:Montserrat,Arial,sans-serif; font-weight:600; text-transform:uppercase; letter-spacing:.04em; }}
.hero .bar {{ width:120px; height:7px; background:{GREEN}; margin:12px 0 8px; }}
.hero .note {{ font-size:13px; opacity:.85; }}
.sq {{ position:absolute; display:block; }}
.tag {{ display:inline-block; background:{NAVY}; color:{GREEN}; font-family:Montserrat,Arial,sans-serif; font-weight:800; font-size:13px; letter-spacing:.06em; text-transform:uppercase; padding:5px 10px; margin:6px 0 12px; }}
.fixed {{ background:#fff; border:1.5px solid #DCE1EC; border-radius:9px; padding:12px 14px; margin-bottom:10px; }}
.fixed .k {{ font-size:12px; color:#5B6782; font-weight:700; text-transform:uppercase; letter-spacing:.04em; }}
.fixed .v {{ font-family:Montserrat,Arial,sans-serif; font-weight:800; font-size:18px; color:{NAVY}; }}
.fixed .h {{ font-size:12px; color:#5B6782; }}
.src {{ display:inline-block; font-size:11px; font-weight:700; color:{BLUE}; background:#E8F0FF; border-radius:4px; padding:2px 6px; margin-left:6px; vertical-align:middle; }}
.cuota {{ display:flex; align-items:center; gap:14px; border:1.5px solid #DCE1EC; border-radius:9px; padding:11px 14px; margin-bottom:8px; background:#fff; }}
.cuota.first {{ border-color:{BLUE}; background:#F2F7FF; }}
.cuota .n {{ min-width:44px; height:44px; border-radius:8px; background:{NAVY}; color:{GREEN}; display:flex; align-items:center; justify-content:center; font-family:Montserrat,Arial,sans-serif; font-weight:800; font-size:18px; }}
.cuota .t {{ font-weight:700; color:{NAVY}; }}
.cuota .d {{ font-size:12.5px; color:#5B6782; }}
.cuota .m {{ margin-left:auto; font-family:Montserrat,Arial,sans-serif; font-weight:800; font-size:19px; color:{NAVY}; white-space:nowrap; }}
.total {{ display:flex; justify-content:space-between; align-items:center; background:{NAVY}; color:#fff; border-radius:9px; padding:15px 18px; margin:10px 0 14px; }}
.total .l {{ font-family:Montserrat,Arial,sans-serif; font-weight:700; text-transform:uppercase; letter-spacing:.05em; font-size:14px; }}
.total .m {{ font-family:Montserrat,Arial,sans-serif; font-weight:800; font-size:26px; color:{GREEN}; }}
.step {{ display:flex; gap:14px; background:#fff; border-left:5px solid {GREEN}; border-radius:6px; padding:12px 14px; margin-bottom:8px; }}
.step .i {{ min-width:30px; height:30px; border-radius:50%; background:{BLUE}; color:#fff; font-weight:800; display:flex; align-items:center; justify-content:center; font-family:Montserrat,Arial,sans-serif; }}
.step .ti {{ font-weight:700; color:{NAVY}; margin-bottom:2px; }}
.step .tx {{ font-size:14px; color:#2B3754; }}
.disc {{ font-size:12.5px; color:#5B6782; border-left:4px solid {GREEN}; padding:6px 12px; margin-top:16px; }}
</style>
""", unsafe_allow_html=True)

# --- Datos del alumno (en producción vienen de la sesión en la web de pagos) ---
with st.sidebar:
    st.markdown("**Modo demostración**")
    st.caption("En la web de pagos virtuales estos datos llegan del sistema al iniciar sesión. "
               "Aquí puedes elegir un alumno de ejemplo para ver los dos casos.")
    caso = st.radio("Alumno de ejemplo", list(ALUMNOS_DEMO), label_visibility="collapsed")
alumno = ALUMNOS_DEMO[caso]

st.markdown(f"""
<div class="hero">
  <div class="brand">Universidad<br>del Pacífico</div>
  <h1>Simulador de cuotas</h1>
  <div class="sub">Pregrado · {PERIODO}</div>
  <div class="bar"></div>
  <div class="note">Conoce cuánto pagarás en cada cuota y cómo se calcula cada monto.</div>
  <span class="sq" style="right:120px;top:30px;width:34px;height:20px;background:{MAGENTA}"></span>
  <span class="sq" style="right:60px;top:62px;width:56px;height:20px;background:{CYAN}"></span>
  <span class="sq" style="right:170px;top:98px;width:26px;height:18px;background:{BLUE}"></span>
  <span class="sq" style="right:40px;bottom:20px;width:40px;height:16px;background:{GREEN}"></span>
</div>
""", unsafe_allow_html=True)

col_in, col_out = st.columns([1, 1.6], gap="large")

with col_in:
    st.markdown('<div class="tag">1. Tus datos</div>', unsafe_allow_html=True)
    valor = ESCALAS[alumno.escala]
    st.markdown(f"""
    <div class="fixed"><div class="k">Tu escala <span class="src">Asignada por el sistema</span></div>
      <div class="v">Escala {alumno.escala}</div><div class="h">{soles(valor)} por crédito</div></div>
    <div class="fixed"><div class="k">Derecho de matrícula <span class="src">Monto fijo</span></div>
      <div class="v">{soles(DERECHO_MATRICULA)}</div><div class="h">Se cobra una sola vez, en la cuota 1.</div></div>
    """, unsafe_allow_html=True)

    if alumno.tiene_matricula:
        st.markdown(f"**Tus cursos matriculados en {PERIODO}** "
                    f'<span class="src">Tomado de tu matrícula</span>', unsafe_allow_html=True)
        st.dataframe(
            [{"Curso": f"{c.codigo} · {c.nombre}", "Tipo": "Taller" if c.es_taller else "Curso",
              "Créditos": c.creditos} for c in alumno.cursos],
            hide_index=True, width="stretch",
        )
        creditos_cursos, creditos_talleres = alumno.creditos_cursos, alumno.creditos_talleres
        st.caption(f"Créditos de cursos: **{fmt(creditos_cursos)}** · Créditos de talleres: **{fmt(creditos_talleres)}**")
    else:
        st.info(f"Aún no tienes matrícula registrada para {PERIODO}. Ingresa los créditos que piensas llevar "
                "para estimar tus cuotas.")
        creditos_cursos = st.number_input("Créditos de cursos", min_value=0.0, max_value=40.0, value=20.0,
                                          step=PASO_CREDITOS, format="%.1f",
                                          help="Suma de créditos de tus cursos, sin contar talleres.")
        creditos_talleres = st.number_input("Créditos de talleres (extra académicos)", min_value=0.0, max_value=10.0,
                                            value=1.0, step=PASO_CREDITOS, format="%.1f")

r = calcular(alumno.escala, creditos_cursos, creditos_talleres)

with col_out:
    st.markdown('<div class="tag">2. Tus cuotas</div>', unsafe_allow_html=True)
    for e in r.errores:
        st.error(e)
    for w in r.advertencias:
        st.warning(w)
    if not r.errores:
        html = []
        for c in r.cuotas:
            html.append(f'<div class="cuota{" first" if c.numero == 1 else ""}"><div class="n">{c.numero}</div>'
                        f'<div><div class="t">Cuota {c.numero}</div><div class="d">{c.glosa}</div></div>'
                        f'<div class="m">{soles(c.monto)}</div></div>')
        html.append(f'<div class="total"><span class="l">Total del periodo</span><span class="m">{soles(r.total)}</span></div>')
        st.markdown("".join(html), unsafe_allow_html=True)

if not r.errores:
    st.markdown('<div class="tag">3. ¿Cómo se calcula tu boleta?</div>', unsafe_allow_html=True)
    st.markdown("".join(
        f'<div class="step"><div class="i">{n}</div><div><div class="ti">{t}</div><div class="tx">{x}</div></div></div>'
        for n, (t, x) in enumerate(explicacion(r), start=1)), unsafe_allow_html=True)

    st.markdown('<div class="tag">4. Guarda tu simulación</div>', unsafe_allow_html=True)
    st.download_button("Descargar resumen en PDF", data=generar_pdf(r, PERIODO),
                       file_name=f"Simulacion_cuotas_{PERIODO}.pdf", mime="application/pdf", type="primary")
    st.markdown("**Resumen para copiar**")
    st.code(resumen_texto(r), language=None)

st.markdown('<div class="disc">Montos referenciales. Los importes definitivos son los que figuran en tu boleta.</div>',
            unsafe_allow_html=True)
