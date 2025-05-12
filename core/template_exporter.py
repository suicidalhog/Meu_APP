# core/template_exporter.py
from fpdf import FPDF
from core.database import Database
import os
from datetime import datetime

def export_template_pdf(transtorno):
    db = Database()
    template = db.buscar_template_por_transtorno(transtorno)
    if not template:
        return

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.set_font("Arial", style='B', size=16)
    pdf.cell(0, 10, f"Template: {transtorno}", ln=True, align="C")
    pdf.ln(10)

    pdf.set_font("Arial", style='B', size=12)
    pdf.cell(40, 10, "Tipo")
    pdf.cell(60, 10, "Rótulo")
    pdf.cell(40, 10, "Variável")
    pdf.cell(20, 10, "Linhas")
    pdf.ln()

    pdf.set_font("Arial", size=11)
    for linha in template.split("\n"):
        if not linha.strip():
            continue
        tipo, rotulo, variavel, *resto = linha.split(",")
        linhas = resto[0] if resto else "1"
        pdf.cell(40, 8, tipo.strip())
        pdf.cell(60, 8, rotulo.strip())
        pdf.cell(40, 8, variavel.strip())
        pdf.cell(20, 8, linhas.strip())
        pdf.ln()

    pdf.ln(10)
    pdf.set_font("Arial", style='I', size=10)
    pdf.cell(0, 10, "Observações: _____________________________________________", ln=True)
    pdf.cell(0, 10, "____________________________________________________________________", ln=True)

    output_dir = os.path.join("exportados", "templates")
    os.makedirs(output_dir, exist_ok=True)
    filename = f"template_{transtorno.replace(' ', '_')}_{datetime.now().strftime('%Y%m%d%H%M%S')}.pdf"
    filepath = os.path.join(output_dir, filename)
    pdf.output(filepath)
    print(f"PDF gerado: {filepath}")

    try:
        if os.name == "nt":
            os.startfile(filepath)
        elif os.name == "posix":
            os.system(f"xdg-open '{filepath}'")
    except Exception as e:
        print(f"Erro ao abrir o PDF: {e}")

    return filepath
