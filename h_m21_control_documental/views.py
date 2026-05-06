from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import DocumentoSGC
from .forms import DocumentoSGCForm


@login_required
def dashboard(request):
    documentos = DocumentoSGC.objects.all().order_by('codigo', '-version')
    return render(request, 'h_m21_control_documental/dashboard.html', {'documentos': documentos})


@login_required
def crear_documento(request):
    if request.method == 'POST':
        form = DocumentoSGCForm(request.POST)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.elaborado_por = request.user
            doc.version = 1  # Por defecto siempre inicia en versión 1
            doc.save()
            messages.success(request, "Documento maestro registrado exitosamente.")
            return redirect('m21_dashboard')
    else:
        form = DocumentoSGCForm(initial={'estado': 'BORRADOR'})
    return render(request, 'h_m21_control_documental/formulario.html', {'form': form, 'accion': 'Registrar Nuevo'})


@login_required
def editar_documento(request, pk):
    doc = get_object_or_404(DocumentoSGC, pk=pk)

    # Bloqueo de auditoría: Un documento obsoleto no se edita jamás
    if doc.estado == 'OBSOLETO':
        messages.error(request, "Los documentos OBSOLETOS están bloqueados por trazabilidad y no pueden modificarse.")
        return redirect('m21_dashboard')

    if request.method == 'POST':
        form = DocumentoSGCForm(request.POST, instance=doc)
        if form.is_valid():
            doc_actualizado = form.save(commit=False)

            # Validación ISO 17025 Cláusula 8.3.2 a): No puede ser Vigente si no tiene aprobación
            if doc_actualizado.estado == 'VIGENTE' and not doc_actualizado.aprobado_por:
                messages.warning(request, "Para pasar a VIGENTE, el documento debe contar con firma de aprobación.")
                return render(request, 'h_m21_control_documental/formulario.html',
                              {'form': form, 'accion': 'Editar / Evaluar'})

            doc_actualizado.save()
            messages.success(request, "Documento actualizado correctamente.")
            return redirect('m21_dashboard')
    else:
        # Bloquear edición del código si no es borrador
        form = DocumentoSGCForm(instance=doc)
        if doc.estado != 'BORRADOR':
            form.fields['codigo'].disabled = True

    return render(request, 'h_m21_control_documental/formulario.html',
                  {'form': form, 'accion': f'Editar v{doc.version}'})


@login_required
def generar_nueva_version(request, pk):
    """
    ISO 17025 Cláusula 8.3.2 f): Retira el actual y genera un borrador clonado con versión +1
    """
    doc_original = get_object_or_404(DocumentoSGC, pk=pk)

    if doc_original.estado != 'VIGENTE':
        messages.error(request, "Solo se pueden generar revisiones de documentos VIGENTES.")
        return redirect('m21_dashboard')

    # El original pasa a Obsoleto para prevenir su uso
    doc_original.estado = 'OBSOLETO'
    doc_original.save()

    # Se clona el registro en base de datos
    doc_original.pk = None
    doc_original.version += 1
    doc_original.estado = 'BORRADOR'
    doc_original.fecha_aprobacion = None
    doc_original.revisado_por = None
    doc_original.aprobado_por = None
    doc_original.descripcion_cambios = ""
    doc_original.elaborado_por = request.user
    doc_original.save()

    messages.success(request,
                     f"El documento anterior fue marcado como OBSOLETO. Se ha generado el borrador para la v{doc_original.version}.")
    return redirect('m21_editar', pk=doc_original.pk)