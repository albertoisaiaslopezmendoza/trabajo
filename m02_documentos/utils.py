import io
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch


def generar_pdf_documento(doc):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=LETTER)
    w, h = LETTER
    margin = 0.65 * inch
    y = h - margin

    def line(txt, size=10, dy=14, bold=False):
        nonlocal y
        c.setFont("Helvetica-Bold" if bold else "Helvetica", size)
        c.drawString(margin, y, str(txt))
        y -= dy

    # Encabezado
    line("DOCUMENTO CONTROLADO — SGC ISO/IEC 17025", 12, 18, bold=True)
    line(f"Título: {doc.titulo}", 11, 16, bold=True)
    line(f"Código: {doc.codigo}    Tipo: {doc.tipo_documento}    Versión: {doc.version}", 10, 14)
    line(f"Área: {doc.area}    Fecha emisión: {doc.fecha_emision}    Vigencia: {doc.vigencia_meses} meses", 10, 14)
    line(f"Estado: {doc.get_estado_display()}", 10, 18, bold=True)

    # Aprobaciones
    line("Aprobación", 11, 16, bold=True)
    elab = doc.elaboro.get_full_name() if doc.elaboro else "Sin asignar"
    rev = doc.reviso.get_full_name() if doc.reviso else "Sin asignar"
    aprob = doc.aprobo.get_full_name() if doc.aprobo else "Sin asignar"

    line(f"Elaboró: {elab}  Fecha: {doc.fecha_firma_elaboro or ''}", 10, 14)
    line(f"Revisó:  {rev}   Fecha: {doc.fecha_firma_reviso or ''}", 10, 14)
    line(f"Aprobó:  {aprob}   Fecha: {doc.fecha_firma_aprobo or ''}", 10, 18)

    # Secciones
    campos = [
        ("1. Objetivo", doc.objetivo),
        ("2. Alcance", doc.alcance),
        ("3. Responsabilidades", doc.responsabilidades),
        ("4. Definiciones y abreviaturas", doc.definiciones),
        ("5. Desarrollo / Procedimiento", doc.procedimiento),
        ("6. Registros generados", doc.registros),
        ("7. Referencias", doc.referencias),
        ("8. Anexos", doc.anexos),
    ]

    for titulo, contenido in campos:
        if y < margin + 120:
            c.showPage()
            y = h - margin
        line(titulo, 11, 16, bold=True)

        text = (contenido or "").strip()
        if not text:
            line("(Sin contenido)", 9, 12)
            y -= 6
            continue

        c.setFont("Helvetica", 9)
        maxw = w - 2 * margin
        words = text.replace("\r", "").split()
        cur_line = ""
        for ww in words:
            test = (cur_line + " " + ww).strip()
            if c.stringWidth(test, "Helvetica", 9) <= maxw:
                cur_line = test
            else:
                c.drawString(margin, y, cur_line)
                y -= 12
                cur_line = ww
                if y < margin + 60:
                    c.showPage()
                    y = h - margin
                    c.setFont("Helvetica", 9)
        if cur_line:
            c.drawString(margin, y, cur_line)
            y -= 14

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer