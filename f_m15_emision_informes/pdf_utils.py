from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors


def generar_informe_pdf(informe, response):
    """
    Genera un PDF básico usando ReportLab.
    Se inyecta en el objeto 'response' de Django.
    """
    p = canvas.Canvas(response, pagesize=letter)
    ancho, alto = letter

    # Encabezado
    p.setFont("Helvetica-Bold", 16)
    p.drawString(50, alto - 50, f"LABCOR - {informe.get_tipo_display()}")

    p.setFont("Helvetica", 12)
    p.drawString(50, alto - 80, f"Código: {informe.codigo_informe}")
    p.drawString(50, alto - 100, f"Estado: {informe.get_estado_display()}")

    if informe.es_enmienda and informe.informe_original:
        p.setFillColor(colors.red)
        p.drawString(50, alto - 120,
                     f"ESTE DOCUMENTO ES UNA ENMIENDA AL INFORME: {informe.informe_original.codigo_informe}")
        p.setFillColor(colors.black)

    # Cuerpo
    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, alto - 160, "Declaración de Conformidad:")
    p.setFont("Helvetica", 10)
    p.drawString(50, alto - 180, informe.declaracion_conformidad or "N/A")

    p.setFont("Helvetica-Bold", 12)
    p.drawString(50, alto - 220, "Opiniones e Interpretaciones:")
    p.setFont("Helvetica", 10)
    p.drawString(50, alto - 240, informe.opiniones_interpretaciones or "N/A")

    # Trazabilidad y Firmas (Simuladas para el PDF)
    p.line(50, 150, 200, 150)
    p.drawString(50, 135, f"Creado por: {informe.creado_por.username if informe.creado_por else 'N/A'}")

    p.line(230, 150, 380, 150)
    p.drawString(230, 135, f"Revisado por: {informe.revisado_por.username if informe.revisado_por else 'Pendiente'}")

    p.line(410, 150, 560, 150)
    p.drawString(410, 135, f"Aprobado por: {informe.aprobado_por.username if informe.aprobado_por else 'Pendiente'}")

    p.showPage()
    p.save()