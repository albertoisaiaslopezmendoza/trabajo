import io
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.utils import timezone
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors

from .models import Capacitacion, AutorizacionMetodo
from .forms import CapacitacionForm, AutorizacionForm


@login_required
def dashboard_competencia(request):
    autorizaciones = AutorizacionMetodo.objects.filter(esta_activo=True)
    capacitaciones = Capacitacion.objects.all().order_by('-fecha_inicio')
    return render(request, 'e_m06_competencia_personal/dashboard.html', {
        'autorizaciones': autorizaciones,
        'capacitaciones': capacitaciones
    })


@login_required
def registrar_autorizacion(request):
    if request.method == 'POST':
        form = AutorizacionForm(request.POST)
        if form.is_valid():
            aut = form.save(commit=False)
            aut.autorizado_por = request.user
            aut.save()
            return redirect('e_m06_dashboard')
    else:
        form = AutorizacionForm()
    return render(request, 'e_m06_competencia_personal/form_autorizacion.html', {'form': form})


@login_required
def descargar_certificado_competencia(request, usuario_id):
    tecnico = get_object_or_404(User, id=usuario_id)
    autorizaciones = AutorizacionMetodo.objects.filter(personal=tecnico, esta_activo=True)

    response = HttpResponse(content_type='application/pdf')
    nombre_archivo = f"Certificado_ISO17025_{tecnico.username}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{nombre_archivo}"'

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # Cabecera
    p.setFont("Helvetica-Bold", 16)
    p.drawCentredString(width / 2, height - 70, "LABCOR - LABORATORIO DE CORROSIÓN")
    p.setFont("Helvetica-Bold", 12)
    p.drawCentredString(width / 2, height - 90, "CERTIFICADO DE COMPETENCIA TÉCNICA (ISO/IEC 17025)")
    p.line(50, height - 100, width - 50, height - 100)

    # Cuerpo
    p.setFont("Helvetica", 11)
    p.drawString(70, height - 140, f"Por la presente se certifica que el analista:")
    p.setFont("Helvetica-Bold", 12)
    p.drawString(70, height - 160, f"{tecnico.get_full_name() or tecnico.username}")

    p.setFont("Helvetica", 11)
    p.drawString(70, height - 190, "Cuenta con la autorización vigente para realizar los siguientes Ensayos / SOPs:")

    # Tabla
    y = height - 220
    p.setFont("Helvetica-Bold", 10)
    p.drawString(70, y, "Código")
    p.drawString(150, y, "Método / SOP")
    p.drawString(450, y, "Fecha Autorización")
    p.line(70, y - 2, width - 70, y - 2)

    y -= 20
    p.setFont("Helvetica", 10)
    for aut in autorizaciones:
        p.drawString(70, y, aut.metodo.codigo)
        p.drawString(150, y, aut.metodo.titulo[:50])
        p.drawString(450, y, aut.fecha_autorizacion.strftime("%d/%m/%Y"))
        y -= 15

    # Firmas
    p.line(100, 150, 250, 150)
    p.drawCentredString(175, 135, "Firma del Técnico")
    p.line(350, 150, 500, 150)
    p.drawCentredString(425, 135, "Director / Gestión Calidad")

    p.setFont("Helvetica-Oblique", 8)
    p.drawString(70, 50, f"Generado el {timezone.now().strftime('%d/%m/%Y %H:%M')}. Documento electrónico controlado.")

    p.showPage()
    p.save()
    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response