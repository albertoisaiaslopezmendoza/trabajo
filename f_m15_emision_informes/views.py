from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import InformeCertificado
from .forms import InformeCertificadoForm
from .pdf_utils import generar_informe_pdf


@login_required
def dashboard(request):
    informes = InformeCertificado.objects.all().order_by('-fecha_creacion')
    return render(request, 'f_m15_emision_informes/dashboard.html', {'informes': informes})


@login_required
def crear_informe(request):
    if request.method == 'POST':
        form = InformeCertificadoForm(request.POST)
        if form.is_valid():
            informe = form.save(commit=False)
            informe.creado_por = request.user
            informe.save()
            messages.success(request, "Informe creado exitosamente.")
            return redirect('m15_dashboard')
    else:
        form = InformeCertificadoForm()
    return render(request, 'f_m15_emision_informes/formulario.html', {'form': form, 'accion': 'Crear'})


@login_required
def editar_informe(request, pk):
    informe = get_object_or_404(InformeCertificado, pk=pk)

    # BLOQUEO ESTRICTO DE EDICIÓN
    if informe.estado in ['APROBADO', 'EMITIDO']:
        messages.error(request, "No se puede editar un informe Aprobado o Emitido. Debe generar una enmienda.")
        return redirect('m15_dashboard')

    if request.method == 'POST':
        form = InformeCertificadoForm(request.POST, instance=informe)
        if form.is_valid():
            form.save()
            messages.success(request, "Informe actualizado exitosamente.")
            return redirect('m15_dashboard')
    else:
        form = InformeCertificadoForm(instance=informe)
    return render(request, 'f_m15_emision_informes/formulario.html', {'form': form, 'accion': 'Editar'})


@login_required
def generar_enmienda(request, pk):
    """Clona un informe emitido y lo prepara como borrador de enmienda"""
    informe_original = get_object_or_404(InformeCertificado, pk=pk)

    if informe_original.estado != 'EMITIDO':
        messages.warning(request, "Solo se pueden generar enmiendas de informes ya emitidos.")
        return redirect('m15_dashboard')

    # Cambiar estado del original a Cancelado/Modificado por trazabilidad
    informe_original.estado = 'CANCELADO'
    informe_original.save()

    # Clonar el informe
    informe_original.pk = None  # Al quitar el PK, Django creará un nuevo registro al hacer save()
    informe_original.codigo_informe = f"{informe_original.codigo_informe}-E1"  # Sufijo de enmienda
    informe_original.estado = 'BORRADOR'
    informe_original.es_enmienda = True
    informe_original.informe_original_id = pk
    informe_original.creado_por = request.user
    informe_original.revisado_por = None
    informe_original.aprobado_por = None
    informe_original.save()

    messages.success(request,
                     f"Enmienda generada: {informe_original.codigo_informe}. Por favor, edite los datos necesarios.")
    return redirect('m15_editar', pk=informe_original.pk)


@login_required
def descargar_pdf(request, pk):
    informe = get_object_or_404(InformeCertificado, pk=pk)

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="LABCOR_Informe_{informe.codigo_informe}.pdf"'

    # Llama a la función que usa ReportLab
    generar_informe_pdf(informe, response)

    return response