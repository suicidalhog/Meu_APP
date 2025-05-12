# core/pdf_exporter.py
from fpdf import FPDF
from core.database import Database
from datetime import datetime
import os
import platform
import subprocess

def export_patient_consultas_pdf(nome_paciente):
    db = Database()
    consultas = db.buscar_historico(nome_paciente)

    if not consultas:
        return

    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)

    pdf.set_font("Arial", 'B', 16)
    pdf.cell(0, 10, f"Histórico de {nome_paciente}", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", size=12)
    for data, nota in consultas:
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, f"{data}", ln=True)
        pdf.set_font("Arial", size=12)
        for linha in nota.split("\n"):
            pdf.multi_cell(0, 8, linha)
        pdf.ln(5)

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"{nome_paciente.replace(' ', '_')}_consultas{len(consultas)}_{timestamp}.pdf"
    output_dir = os.path.join("exportados", "pdfs")
    os.makedirs(output_dir, exist_ok=True)
    filepath = os.path.join(output_dir, filename)

    pdf.output(filepath)
    print(f"PDF exportado: {filepath}")

    try:
        if platform.system() == "Windows":
            os.startfile(filepath)
        elif platform.system() == "Darwin":
            subprocess.run(["open", filepath])
        else:
            subprocess.run(["xdg-open", filepath])
    except Exception as e:
        print(f"Erro ao abrir o PDF: {e}")

    return filepath
