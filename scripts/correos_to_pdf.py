#!/usr/bin/env python3
"""
Genera un PDF con tabla de correos enviados a partir de datos JSON.

Uso:
    python3 scripts/correos_to_pdf.py <json_input> <pdf_output>

Input JSON:
    {
        "entidad": "IDT",
        "periodo_inicio": "2026-02-01",
        "periodo_fin": "2026-02-28",
        "cuenta": "usuario@entidad.gov.co",
        "total": 15,
        "correos": [
            {
                "num": 1,
                "fecha": "2026-02-05",
                "asunto": "RE: Error modulo X",
                "destinatarios": "usuario@entidad.gov.co",
                "tipo": "Soporte",
                "resumen": "Se indico solucion al error reportado..."
            }
        ]
    }
"""

import json
import os
import sys
from datetime import datetime

from fpdf import FPDF


class CorreosPDF(FPDF):
    """PDF personalizado para reporte de correos."""

    def __init__(self, entidad, periodo_inicio, periodo_fin, cuenta):
        super().__init__(orientation="L", format="A4")
        self.entidad = entidad
        self.periodo_inicio = periodo_inicio
        self.periodo_fin = periodo_fin
        self.cuenta = cuenta

    def header(self):
        self.set_font("Helvetica", "B", 14)
        self.set_fill_color(0, 51, 102)
        self.set_text_color(255, 255, 255)
        self.cell(0, 10, f"REPORTE DE CORREOS ENVIADOS - {self.entidad}", align="C", fill=True, new_x="LMARGIN", new_y="NEXT")
        self.set_font("Helvetica", "", 9)
        self.set_text_color(60, 60, 60)
        self.cell(0, 6, f"Periodo: {self.periodo_inicio} a {self.periodo_fin}  |  Cuenta: {self.cuenta}", align="C", new_x="LMARGIN", new_y="NEXT")
        self.ln(3)

    def footer(self):
        self.set_y(-15)
        self.set_font("Helvetica", "I", 7)
        self.set_text_color(128, 128, 128)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        self.cell(0, 10, f"Generado automaticamente el {timestamp}  |  Pagina {self.page_no()}/{{nb}}", align="C")


def truncate_text(text, max_len):
    """Trunca texto a max_len caracteres."""
    if not text:
        return ""
    text = str(text).replace("\n", " ").replace("\r", "")
    if len(text) > max_len:
        return text[:max_len - 3] + "..."
    return text


def generate_pdf(data, output_path):
    """Genera el PDF a partir de los datos JSON."""
    entidad = data.get("entidad", "")
    periodo_inicio = data.get("periodo_inicio", "")
    periodo_fin = data.get("periodo_fin", "")
    cuenta = data.get("cuenta", "")
    total = data.get("total", 0)
    correos = data.get("correos", [])

    pdf = CorreosPDF(entidad, periodo_inicio, periodo_fin, cuenta)
    pdf.alias_nb_pages()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    # Resumen
    pdf.set_font("Helvetica", "B", 10)
    pdf.set_text_color(0, 0, 0)
    pdf.cell(0, 7, f"Total de correos enviados: {total}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(3)

    # Columnas: #, Fecha, Asunto, Destinatarios, Tipo, Resumen
    col_widths = [10, 22, 75, 60, 25, 85]
    col_headers = ["#", "Fecha", "Asunto", "Destinatarios", "Tipo", "Resumen"]

    # Header de tabla
    pdf.set_font("Helvetica", "B", 7)
    pdf.set_fill_color(0, 51, 102)
    pdf.set_text_color(255, 255, 255)
    for i, header in enumerate(col_headers):
        pdf.cell(col_widths[i], 7, header, border=1, fill=True, align="C")
    pdf.ln()

    # Filas
    pdf.set_font("Helvetica", "", 7)
    pdf.set_text_color(0, 0, 0)

    for idx, correo in enumerate(correos):
        # Sombreado alternado
        if idx % 2 == 0:
            pdf.set_fill_color(245, 245, 245)
            fill = True
        else:
            pdf.set_fill_color(255, 255, 255)
            fill = True

        num = str(correo.get("num", idx + 1))
        fecha = str(correo.get("fecha", ""))[:10]
        asunto = truncate_text(correo.get("asunto", ""), 55)
        destinatarios = truncate_text(correo.get("destinatarios", ""), 42)
        tipo = truncate_text(correo.get("tipo", ""), 18)
        resumen = truncate_text(correo.get("resumen", ""), 62)

        row_data = [num, fecha, asunto, destinatarios, tipo, resumen]
        aligns = ["C", "C", "L", "L", "C", "L"]

        for i, val in enumerate(row_data):
            pdf.cell(col_widths[i], 6, val, border=1, fill=fill, align=aligns[i])
        pdf.ln()

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    pdf.output(output_path)
    print(f"PDF generado: {output_path} ({len(correos)} correos)", file=sys.stderr)


def main():
    if len(sys.argv) < 3:
        print("Uso: python3 scripts/correos_to_pdf.py <json_input> <pdf_output>")
        sys.exit(1)

    json_input = sys.argv[1]
    pdf_output = sys.argv[2]

    with open(json_input, "r", encoding="utf-8") as f:
        data = json.load(f)

    generate_pdf(data, pdf_output)


if __name__ == "__main__":
    main()
