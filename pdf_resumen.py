"""Genera el resumen imprimible (PDF) de la simulación con fpdf2."""
from datetime import datetime

from fpdf import FPDF

from calculo import Resultado, explicacion, fmt, soles

NAVY, GREEN, BLUE, GREY = (14, 31, 67), (0, 255, 36), (0, 98, 255), (91, 103, 130)


def _t(s: str) -> str:
    """Las fuentes base de PDF usan Latin-1: reemplaza los pocos caracteres que no entran."""
    return (s.replace("–", "-").replace("—", "-").replace("“", '"').replace("”", '"')
             .replace("‘", "'").replace("’", "'").replace("…", "..."))


def generar_pdf(r: Resultado, periodo: str, nombre_alumno: str = "") -> bytes:
    pdf = FPDF(format="A4")
    pdf.set_auto_page_break(True, margin=18)
    pdf.add_page()
    W = pdf.w - 2 * pdf.l_margin

    # Encabezado
    pdf.set_fill_color(*NAVY)
    pdf.rect(0, 0, pdf.w, 46, "F")
    for x, y, w, h, c in [(170, 9, 9, 5, (215, 51, 255)), (182, 16, 14, 5, (97, 242, 242)), (164, 23, 7, 4, BLUE)]:
        pdf.set_fill_color(*c); pdf.rect(x, y, w, h, "F")
    pdf.set_xy(pdf.l_margin, 9)
    pdf.set_text_color(255, 255, 255); pdf.set_font("Helvetica", "B", 9)
    pdf.cell(0, 4, "UNIVERSIDAD DEL PACÍFICO", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)
    pdf.set_text_color(*GREEN); pdf.set_font("Helvetica", "B", 22)
    pdf.cell(0, 10, "SIMULADOR DE CUOTAS", new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(255, 255, 255); pdf.set_font("Helvetica", "B", 11)
    pdf.cell(0, 6, _t(f"PREGRADO · {periodo}"), new_x="LMARGIN", new_y="NEXT")
    pdf.set_y(54)

    # Datos
    pdf.set_text_color(*NAVY); pdf.set_font("Helvetica", "", 10)
    datos = [("Escala", f"{r.escala} ({soles(r.valor_credito)} por crédito)"),
             ("Créditos de cursos", fmt(r.creditos_cursos)),
             ("Créditos de talleres", fmt(r.creditos_talleres)),
             ("Derecho de matrícula", soles(r.derecho_matricula))]
    if nombre_alumno:
        datos.insert(0, ("Alumno", nombre_alumno))
    for k, v in datos:
        pdf.set_font("Helvetica", "B", 10); pdf.cell(48, 6, _t(k))
        pdf.set_font("Helvetica", "", 10); pdf.cell(0, 6, _t(v), new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    # Tabla de cuotas
    pdf.set_fill_color(*NAVY); pdf.set_text_color(255, 255, 255); pdf.set_font("Helvetica", "B", 10)
    pdf.cell(22, 8, "Cuota", fill=True); pdf.cell(W - 22 - 38, 8, "Detalle", fill=True)
    pdf.cell(38, 8, "Monto", fill=True, align="R", new_x="LMARGIN", new_y="NEXT")
    pdf.set_text_color(*NAVY)
    for i, c in enumerate(r.cuotas):
        pdf.set_fill_color(242, 247, 255) if i == 0 else pdf.set_fill_color(255, 255, 255)
        pdf.set_font("Helvetica", "B", 10); pdf.cell(22, 9, str(c.numero), fill=True, border="B")
        pdf.set_font("Helvetica", "", 8.5); pdf.cell(W - 22 - 38, 9, _t(c.glosa), fill=True, border="B")
        pdf.set_font("Helvetica", "B", 10)
        pdf.cell(38, 9, soles(c.monto), fill=True, border="B", align="R", new_x="LMARGIN", new_y="NEXT")
    pdf.set_fill_color(*NAVY); pdf.set_text_color(*GREEN); pdf.set_font("Helvetica", "B", 12)
    pdf.cell(W - 45, 11, "  TOTAL DEL PERIODO", fill=True)
    pdf.cell(45, 11, soles(r.total) + "  ", fill=True, align="R", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(6)

    # Explicación
    pdf.set_text_color(*NAVY); pdf.set_font("Helvetica", "B", 12)
    pdf.cell(0, 7, _t("¿Cómo se calcula tu boleta?"), new_x="LMARGIN", new_y="NEXT")
    for n, (titulo, texto) in enumerate(explicacion(r), start=1):
        pdf.set_font("Helvetica", "B", 10); pdf.multi_cell(W, 5.5, _t(f"{n}. {titulo}"), new_x="LMARGIN", new_y="NEXT")
        pdf.set_font("Helvetica", "", 9.5); pdf.multi_cell(W, 5, _t(texto), new_x="LMARGIN", new_y="NEXT")
        pdf.ln(1.5)
    for w in r.advertencias:
        pdf.set_text_color(138, 90, 0); pdf.set_font("Helvetica", "B", 9)
        pdf.multi_cell(W, 5, _t("Atención: " + w), new_x="LMARGIN", new_y="NEXT")

    pdf.ln(4)
    pdf.set_text_color(*GREY); pdf.set_font("Helvetica", "", 8.5)
    pdf.multi_cell(W, 4.5, _t("Montos referenciales. Los importes definitivos son los que figuran en tu boleta. "
                              f"Simulación generada el {datetime.now():%d/%m/%Y %H:%M}."), new_x="LMARGIN", new_y="NEXT")
    pdf.set_fill_color(*BLUE); pdf.rect(0, pdf.h - 6, pdf.w, 6, "F")
    return bytes(pdf.output())
