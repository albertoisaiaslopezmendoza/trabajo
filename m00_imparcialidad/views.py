import base64
import uuid
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from .models import DeclaracionImparcialidad
from .forms import DeclaracionForm

# Importaciones para PDF (se mantienen igual que antes)
import io
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image as RLImage
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors


@login_required
def dashboard_m00(request):
    declaraciones = DeclaracionImparcialidad.objects.filter(usuario=request.user).order_by('-created_at')[:10]
    return render(request, 'm00_imparcialidad/dashboard.html', {'declaraciones': declaraciones})


@login_required
def crear_declaracion(request):
    if request.method == 'POST':
        form = DeclaracionForm(request.POST)
        if form.is_valid():
            decl = form.save(commit=False)
            decl.usuario = request.user

            # --- PROCESAR FIRMA DRAWING (BASE64) ---
            data_url = form.cleaned_data['firma_data_url']
            # El formato viene como "data:image/png;base64,iVBORw0KGgoAAA..."
            format, imgstr = data_url.split(';base64,')
            ext = format.split('/')[-1]  # png

            file_name = f"firma_m00_{request.user.id}_{uuid.uuid4()}.{ext}"
            data = ContentFile(base64.b64decode(imgstr), name=file_name)

            decl.firma_imagen = data

            # --- IP y Blockchain Simulado ---
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            decl.ip_origen = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')

            ultimo = DeclaracionImparcialidad.objects.all().order_by('-id').first()
            decl.prev_hash = ultimo.hash_registro if ultimo else "0" * 64

            decl.save()  # Guardar primero para generar ID y ruta

            # Calcular hash final
            decl.hash_registro = decl.calcular_hash(getattr(settings, 'SECRET_KEY', 'demo'))
            decl.save()

            messages.success(request, "Declaración firmada y registrada exitosamente.")
            return redirect('m00_imparcialidad:dashboard')
        else:
            messages.error(request, "Por favor corrija los errores en el formulario.")
    else:
        initial_data = {
            'nombre_completo': f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
        }
        form = DeclaracionForm(initial=initial_data)

    return render(request, 'm00_imparcialidad/form.html', {'form': form})


# La vista descargar_pdf se queda IGUAL que la que ya tenías, funciona bien.
@login_required
def descargar_pdf(request, decl_id):
    # ... (Mantener tu código existente para descargar_pdf) ...
    decl = get_object_or_404(DeclaracionImparcialidad, id=decl_id, usuario=request.user)

    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=LETTER)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph("<b>CONSTANCIA DE IMPARCIALIDAD Y CONFIDENCIALIDAD</b>", styles["Title"]))
    story.append(Spacer(1, 12))
    story.append(Paragraph("M00 — Sistema de Gestión ISO/IEC 17025", styles["Normal"]))
    story.append(Spacer(1, 20))

    data = [
        ["Folio ID", str(decl.id)],
        ["Firmante", decl.nombre_completo],
        ["Puesto", decl.puesto],
        ["Fecha", decl.created_at.strftime("%Y-%m-%d %H:%M")],
        ["Hash Registro", Paragraph(f"<font size=6>{decl.hash_registro}</font>", styles["Normal"])],
    ]

    t = Table(data, colWidths=[100, 350])
    t.setStyle(TableStyle([
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ('BACKGROUND', (0, 0), (0, -1), colors.whitesmoke),
        ('PADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(t)
    story.append(Spacer(1, 20))

    story.append(Paragraph("<b>Declaraciones Aceptadas:</b>", styles["Heading3"]))
    story.append(Paragraph("☑ Imparcialidad, Confidencialidad y Privacidad aceptadas.", styles["Normal"]))
    story.append(Spacer(1, 20))

    story.append(Paragraph("<b>Firma Registrada:</b>", styles["Heading3"]))
    story.append(Spacer(1, 10))

    if decl.firma_imagen:
        try:
            path_imagen = decl.firma_imagen.path
            story.append(RLImage(path_imagen, width=200, height=80, kind='proportional'))
        except Exception:
            story.append(Paragraph("[Error visualizando firma]", styles["Normal"]))

    doc.build(story)
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')