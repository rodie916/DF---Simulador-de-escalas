import streamlit as st

from calculo import CREDITOS_CUOTA_1, DERECHO_ENSENANZA, ESCALAS, calcular

st.set_page_config(page_title="Simulador de cuotas – Pregrado", page_icon="🧮", layout="wide")

NAVY, GREEN, BLUE, CYAN, MAGENTA = "#0E1F43", "#00FF24", "#0062FF", "#61F2F2", "#D733FF"


def soles(x: float) -> str:
    return f"S/ {x:,.2f}"


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
.hero .note {{ font-size:13px; opacity:.8; }}
.sq {{ position:absolute; display:block; }}
.tag {{ display:inline-block; background:{NAVY}; color:{GREEN}; font-family:Montserrat,Arial,sans-serif; font-weight:800; font-size:13px; letter-spacing:.06em; text-transform:uppercase; padding:5px 10px; margin-bottom:10px; }}
.cuota {{ display:flex; align-items:center; gap:14px; border:1.5px solid #DCE1EC; border-radius:9px; padding:11px 14px; margin-bottom:8px; }}
.cuota.first {{ border-color:{BLUE}; background:#F2F7FF; }}
.cuota .n {{ min-width:44px; height:44px; border-radius:8px; background:{NAVY}; color:{GREEN}; display:flex; align-items:center; justify-content:center; font-family:Montserrat,Arial,sans-serif; font-weight:800; font-size:18px; }}
.cuota .t {{ font-weight:700; color:{NAVY}; }}
.cuota .d {{ font-size:12.5px; color:#5B6782; }}
.cuota .m {{ margin-left:auto; font-family:Montserrat,Arial,sans-serif; font-weight:800; font-size:19px; color:{NAVY}; white-space:nowrap; }}
.total {{ display:flex; justify-content:space-between; align-items:center; background:{NAVY}; color:#fff; border-radius:9px; padding:15px 18px; margin-top:10px; margin-bottom:14px; }}
.total .l {{ font-family:Montserrat,Arial,sans-serif; font-weight:700; text-transform:uppercase; letter-spacing:.05em; font-size:14px; }}
.total .m {{ font-family:Montserrat,Arial,sans-serif; font-weight:800; font-size:26px; color:{GREEN}; }}
.disc {{ font-size:12.5px; color:#5B6782; border-left:4px solid {GREEN}; padding:6px 12px; margin-top:16px; }}
div[data-testid="stMetricValue"] {{ font-family:Montserrat,Arial,sans-serif; font-weight:800; color:{NAVY}; font-size:1.35rem; }}
</style>
""", unsafe_allow_html=True)

# --- Estado inicial / restablecer
DEF = {"periodo": "2026-II", "escala": "5", "adm": 21.0, "extra": 1.0, "derecho": DERECHO_ENSENANZA}
for k, v in DEF.items():
    st.session_state.setdefault(k, v)


def restablecer():
    for k, v in DEF.items():
        st.session_state[k] = v


periodo = st.session_state["periodo"] or "—"
st.markdown(f"""
<div class="hero">
  <div class="brand">Universidad<br>del Pacífico</div>
  <h1>Simulador de cuotas</h1>
  <div class="sub">Pregrado · {periodo}</div>
  <div class="bar"></div>
  <div class="note">Herramienta referencial para orientación de estudiantes</div>
  <span class="sq" style="right:120px;top:30px;width:34px;height:20px;background:{MAGENTA}"></span>
  <span class="sq" style="right:60px;top:62px;width:56px;height:20px;background:{CYAN}"></span>
  <span class="sq" style="right:170px;top:98px;width:26px;height:18px;background:{BLUE}"></span>
  <span class="sq" style="right:40px;bottom:20px;width:40px;height:16px;background:{GREEN}"></span>
</div>
""", unsafe_allow_html=True)

col_in, col_out = st.columns([1, 1.7], gap="large")

with col_in:
    st.markdown('<div class="tag">1. Ingresa los datos</div>', unsafe_allow_html=True)
    st.text_input("Periodo académico", key="periodo")
    st.radio(
        "Escala asignada",
        options=list(ESCALAS),
        format_func=lambda k: f"{k}  (S/ {ESCALAS[k]:,})",
        key="escala",
        horizontal=True,
        help="El valor por crédito se actualiza automáticamente.",
    )
    st.number_input("Créditos administrativos", min_value=0.0, step=0.1, format="%.2f", key="adm",
                    help="Total del periodo, incluidos los créditos extra académicos. Mínimo 3.8.")
    c1, c2 = st.columns(2)
    c1.number_input("Créditos extra académicos", min_value=0.0, step=0.1, format="%.2f", key="extra")
    c2.number_input("Derecho de enseñanza (S/)", min_value=0.0, step=1.0, format="%.2f", key="derecho")
    st.button("Restablecer", on_click=restablecer)

r = calcular(st.session_state["escala"], st.session_state["adm"], st.session_state["extra"], st.session_state["derecho"])

with col_out:
    st.markdown('<div class="tag">2. Resultado</div>', unsafe_allow_html=True)
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Escala", st.session_state["escala"])
    m2.metric("Valor por crédito", soles(r.valor_credito))
    m3.metric("Créditos adm.", f"{st.session_state['adm']:.2f}")
    m4.metric("Extra académicos", f"{st.session_state['extra']:.2f}")

    for e in r.errores:
        st.error(e)
    for w in r.advertencias:
        st.warning(w)

    ok = not r.errores
    html = []
    for i, monto in enumerate(r.cuotas, start=1):
        if i == 1:
            det = f"{CREDITOS_CUOTA_1:.2f} créditos × {soles(r.valor_credito)} + {soles(st.session_state['derecho'])} derecho de enseñanza"
        else:
            det = (f"{r.creditos_adm_por_cuota:.2f} créditos administrativos + {r.creditos_extra_por_cuota:.2f} créditos extra académicos "
                   f"({r.creditos_adm_por_cuota + r.creditos_extra_por_cuota:.2f} × {soles(r.valor_credito)})")
        html.append(f'<div class="cuota{" first" if i == 1 else ""}"><div class="n">{i}</div>'
                    f'<div><div class="t">Cuota {i}</div><div class="d">{det}</div></div>'
                    f'<div class="m">{soles(monto) if ok else "—"}</div></div>')
    html.append(f'<div class="total"><span class="l">Total del periodo</span>'
                f'<span class="m">{soles(r.total) if ok else "—"}</span></div>')
    st.markdown("".join(html), unsafe_allow_html=True)

    if ok:
        resumen = "\n".join([
            f"Simulación de cuotas – Pregrado {periodo}",
            f"Escala {st.session_state['escala']} (S/ {r.valor_credito:,.2f} por crédito) · "
            f"{st.session_state['adm']:.2f} créditos administrativos, {st.session_state['extra']:.2f} extra académicos",
            *[f"Cuota {i}: {soles(m)}" for i, m in enumerate(r.cuotas, start=1)],
            f"Total del periodo: {soles(r.total)}",
            "Montos referenciales, sujetos a validación.",
        ])
        with st.expander("Resumen para copiar"):
            st.code(resumen, language=None)

    with st.expander("¿Cómo se calcula?"):
        st.markdown(
            "1. **Cuota 1:** 3.8 créditos administrativos × valor por crédito + derecho de enseñanza.\n"
            "2. **Cuotas 2 a 5:** los créditos administrativos restantes (sin los extra académicos ni los 3.8 de la cuota 1) "
            "se reparten en partes iguales, y el importe de los créditos extra académicos también se divide entre las 4 cuotas.\n"
            "3. Cada cuota se redondea a 2 decimales."
        )
    with st.expander("Escalas de pago 2026"):
        st.table({"Escala": list(ESCALAS), "Valor por crédito (S/)": [f"{v:,.2f}" for v in ESCALAS.values()]})

    st.markdown('<div class="disc">Montos referenciales. Valida los importes definitivos según las disposiciones '
                'institucionales vigentes antes de comunicarlos.</div>', unsafe_allow_html=True)
