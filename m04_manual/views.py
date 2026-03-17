from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from django.http import HttpResponse
from .models import ManualSGC, ManualDistribution
from .forms import ManualSGCForm, DistributionForm

from reportlab.lib.pagesizes import LETTER
from reportlab.pdfgen import canvas
import datetime
import textwrap  # Importación nueva para envolver el texto en el PDF


@login_required
def dashboard(request):
    manuales = ManualSGC.objects.all().order_by('-id')
    manual_actual = manuales.first()

    if request.method == 'POST':
        # Guardar / Actualizar BORRADOR
        if not manual_actual or manual_actual.estado != 'BORRADOR':
            form = ManualSGCForm(request.POST)
        else:
            form = ManualSGCForm(request.POST, instance=manual_actual)

        if form.is_valid():
            manual = form.save(commit=False)
            manual.elaborado_por = request.user.username
            manual.estado = 'BORRADOR'
            manual.proxima_revision = None
            manual.save()
            messages.success(request, 'Manual guardado como BORRADOR.')
            return redirect('m04_manual:dashboard')
    else:
        if manual_actual and manual_actual.estado == 'BORRADOR':
            form = ManualSGCForm(instance=manual_actual)
        else:
            form = ManualSGCForm(instance=manual_actual) if manual_actual else ManualSGCForm()

    dist_form = DistributionForm()

    context = {
        'manual_actual': manual_actual,
        'manuales': manuales,
        'form': form,
        'dist_form': dist_form,
    }
    return render(request, 'm04_manual/dashboard.html', context)


@login_required
def nueva_revision(request):
    # CORRECCIÓN: Evitar creación por petición GET
    if request.method == 'POST':
        manuales = ManualSGC.objects.all().order_by('-id')
        manual_actual = manuales.first()

        if manual_actual:
            nueva_version = f"{manual_actual.version}-rev"
            ManualSGC.objects.create(
                doc_code=manual_actual.doc_code,
                doc_title=manual_actual.doc_title,
                contenido=manual_actual.contenido,
                version=nueva_version,
                estado='BORRADOR',
                cambio_resumen='Nueva revisión',
                elaborado_por=request.user.username,
                fecha_vigencia=datetime.date.today()
            )
            messages.success(request, 'Nueva revisión creada como BORRADOR.')
    return redirect('m04_manual:dashboard')


@login_required
def aprobar_manual(request, pk):
    # CORRECCIÓN: Validar método POST para proteger la aprobación
    if request.method == 'POST':
        manual = get_object_or_404(ManualSGC, pk=pk)
        if manual.estado == 'BORRADOR':
            manual.estado = 'APROBADO'
            manual.aprobado_por = request.user.username
            manual.fecha_aprobacion = timezone.now()
            manual.save()
            messages.success(request, 'El documento ha sido APROBADO exitosamente.')
    return redirect('m04_manual:dashboard')


@login_required
def agregar_distribucion(request, pk):
    manual = get_object_or_404(ManualSGC, pk=pk)
    if request.method == 'POST':
        form = DistributionForm(request.POST)
        if form.is_valid():
            dist = form.save(commit=False)
            dist.manual = manual
            dist.created_by = request.user.username
            if dist.ack_received and not dist.ack_on:
                dist.ack_on = datetime.date.today()
            dist.save()
            messages.success(request, 'Distribución agregada.')
    return redirect('m04_manual:dashboard')


@login_required
def exportar_pdf(request, pk):
    manual = get_object_or_404(ManualSGC, pk=pk)
    distribuciones = manual.distribuciones.filter(copy_type='CONTROLADA')[:10]

    response = HttpResponse(content_type='application/pdf')
    filename = f"{manual.doc_code}_Manual_SGC.pdf".replace("/", "-")
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    c = canvas.Canvas(response, pagesize=LETTER)
    w, h = LETTER

    def draw_header(page_no):
        c.setFont("Helvetica-Bold", 11)
        c.drawString(40, h - 32, f"{manual.doc_code} — {manual.doc_title}")
        c.setFont("Helvetica", 9)
        c.drawString(40, h - 48, f"ISO/IEC 17025 | Versión: {manual.version} | Estatus: {manual.estado}")
        c.drawString(40, h - 62, f"Vigencia: {manual.fecha_vigencia} | Próx. revisión: {manual.proxima_revision}")
        c.drawString(40, h - 76, f"Elaboró: {manual.elaborado_por} | Aprobó: {manual.aprobado_por or 'N/A'}")
        c.setFont("Helvetica", 8)
        c.drawString(40, 22, "Documento controlado — Copia CONTROLADA")
        c.drawRightString(w - 40, 22, f"Página {page_no}")

    # Portada
    c.setFont("Helvetica-Bold", 16)
    c.drawString(40, h - 70, "MANUAL DE CALIDAD")
    c.setFont("Helvetica", 11)
    c.drawString(40, h - 92, "Sistema de Gestión de la Calidad — ISO/IEC 17025")
    c.setFont("Helvetica", 10)
    c.drawString(40, h - 120, f"Código: {manual.doc_code}")
    c.drawString(40, h - 138, f"Título: {manual.doc_title}")
    c.drawString(40, h - 156, f"Versión: {manual.version}   Estatus: {manual.estado}")
    c.drawString(40, h - 174, f"Vigencia: {manual.fecha_vigencia}   Próx. revisión: {manual.proxima_revision}")
    c.drawString(40, h - 192, f"Elaboró: {manual.elaborado_por}   Aprobó: {manual.aprobado_por or 'N/A'}")
    c.drawString(40, h - 240, f"Resumen de cambios: {manual.cambio_resumen[:110]}")

    c.setFont("Helvetica-Bold", 10)
    c.drawString(40, h - 270, "Lista de distribución (copias controladas)")
    c.setFont("Helvetica", 9)
    y = h - 286
    if not distribuciones:
        c.drawString(40, y, "Sin registros de distribución CONTROLADA.")
    else:
        c.drawString(40, y, "Destinatario / Área — Método — Entrega — Acuse")
        y -= 14
        for d in distribuciones:
            ack = "Sí" if d.ack_received else "No"
            line = f"{d.recipient_name} / {d.area} — {d.delivery_method} — {d.delivered_on or ''} — {ack} {d.ack_on or ''}"
            c.drawString(40, y, line[:115])
            y -= 12
    c.showPage()

    # Contenido
    lines = manual.contenido.split("\n")
    page_no = 1
    y = h - 110
    draw_header(page_no)
    c.setFont("Helvetica", 9)

    for line in lines:
        # CORRECCIÓN: textwrap para evitar que el texto se pierda si la línea es muy larga
        wrapped_lines = textwrap.wrap(line, width=105)
        if not wrapped_lines:  # Para manejar los saltos de línea vacíos
            y -= 14
            continue

        for wrapped_line in wrapped_lines:
            if y < 40:
                c.showPage()
                page_no += 1
                y = h - 110
                draw_header(page_no)
                c.setFont("Helvetica", 9)
            c.drawString(40, y, wrapped_line)
            y -= 14

    c.save()
    return response