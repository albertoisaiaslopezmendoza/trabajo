import io
from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
from reportlab.lib.units import mm
from django.core.files.base import ContentFile
from datetime import timedelta
from django.utils import timezone


def calcular_estatus(fecha_limpieza, frecuencia_dias):
    """
    Calcula si el activo está vigente, por vencer o vencido.
    """
    if frecuencia_dias <= 0:
        return "SIN FRECUENCIA", None

    proximo = fecha_limpieza + timedelta(days=frecuencia_dias)
    hoy = timezone.now()
    remaining = (proximo - hoy).total_seconds()

    if remaining < 0:
        return "VENCIDO", proximo

    warn_seconds = max(24 * 3600, int(frecuencia_dias * 0.10 * 24 * 3600))
    if remaining <= warn_seconds:
        return "POR VENCER", proximo

    return "A TIEMPO", proximo


def generar_pdf_evidencia(registro):
    """
    Genera el PDF leyendo los campos de texto plano.
    """
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=LETTER)
    w, h = LETTER

    # Encabezado
    c.setFont("Helvetica-Bold", 14)
    c.drawString(20 * mm, h - 20 * mm, "LABCOR - Evidencia de Limpieza")
    c.setFont("Helvetica", 9)
    c.drawString(20 * mm, h - 26 * mm, "Registro generado desde Plataforma Web - ISO 17025")

    y = h - 40 * mm

    def line(label, val):
        nonlocal y
        c.setFont("Helvetica-Bold", 9)
        c.drawString(20 * mm, y, f"{label}:")
        c.setFont("Helvetica", 9)
        c.drawString(60 * mm, y, str(val or ""))
        y -= 6 * mm

    line("Folio UUID", str(registro.uuid))
    line("Fecha/Hora", registro.fecha_hora.strftime("%Y-%m-%d %H:%M (UTC)"))
    line("Activo", registro.nombre_activo_snapshot)
    line("Área", registro.area_snapshot)

    responsable = registro.realizado_por.username
    if registro.realizado_por.first_name:
        responsable = f"{registro.realizado_por.first_name} {registro.realizado_por.last_name}"
    line("Responsable", responsable)

    line("Estatus calculado", registro.estado)
    if registro.proximo_vencimiento:
        line("Próximo Vencimiento", registro.proximo_vencimiento.strftime("%Y-%m-%d %H:%M"))

    # --- CHECKLIST (Lectura de Texto Plano) ---
    y -= 5 * mm
    c.setFont("Helvetica-Bold", 10)
    c.drawString(20 * mm, y, "Checklist Realizado:")
    y -= 5 * mm
    c.setFont("Helvetica", 9)

    # Obtenemos el texto: "Barrer, Trapear, Sacudir"
    texto_checklist = registro.checklist_realizado

    if texto_checklist:
        # Separamos por comas para hacer una lista bonita en el PDF
        items = texto_checklist.split(',')
        for item in items:
            item_limpio = item.strip()  # Quitamos espacios extra
            if item_limpio:
                c.drawString(25 * mm, y, f"[X] {item_limpio}")
                y -= 5 * mm
    else:
        c.drawString(25 * mm, y, "Ninguna tarea registrada.")

    # --- QUIMICOS ---
    y -= 2 * mm
    c.setFont("Helvetica-Bold", 10)
    c.drawString(20 * mm, y, "Químicos Usados:")
    y -= 5 * mm
    c.setFont("Helvetica", 9)
    c.drawString(25 * mm, y, registro.quimicos_usados or "N/A")

    # Observaciones
    y -= 8 * mm
    c.setFont("Helvetica-Bold", 10)
    c.drawString(20 * mm, y, "Observaciones:")
    y -= 5 * mm
    c.setFont("Helvetica", 9)
    obs = registro.observaciones or "Sin observaciones"
    c.drawString(25 * mm, y, obs[:95])

    c.showPage()
    c.save()

    buffer.seek(0)
    return ContentFile(buffer.getvalue(), name=f"evidencia_{registro.uuid}.pdf")