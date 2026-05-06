from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import RegistroCalidad
from .forms import RegistroCalidadForm


@login_required
def dashboard(request):
    registros = RegistroCalidad.objects.all().order_by('-fecha_creacion_registro')
    return render(request, 'h_m22_control_registros/dashboard.html', {'registros': registros})


@login_required
def crear_registro(request):
    if request.method == 'POST':
        form = RegistroCalidadForm(request.POST)
        if form.is_valid():
            registro = form.save(commit=False)
            # Sello de archivo si nace ya archivado (caso raro pero posible para datos históricos)
            if registro.estado == 'ARCHIVADO':
                registro.fecha_archivo = timezone.now().date()
            registro.save()
            messages.success(request, "Configuración de retención de registro creada exitosamente.")
            return redirect('m22_dashboard')
    else:
        form = RegistroCalidadForm()
    return render(request, 'h_m22_control_registros/formulario.html', {'form': form, 'accion': 'Declarar Nuevo'})


@login_required
def editar_registro(request, pk):
    registro = get_object_or_404(RegistroCalidad, pk=pk)

    # BLOQUEO ISO 17025: Un registro destruido solo puede visualizarse, jamás editarse
    if registro.estado == 'DESTRUIDO':
        messages.error(request,
                       "Este registro ya ha sido DESTRUIDO/ELIMINADO y está bloqueado por trazabilidad. No admite modificaciones.")
        return redirect('m22_dashboard')

    if request.method == 'POST':
        estado_anterior = registro.estado
        form = RegistroCalidadForm(request.POST, instance=registro)
        if form.is_valid():
            reg_actualizado = form.save(commit=False)

            # Lógica de sellado de fechas automatizado según cambio de estados
            if estado_anterior != 'ARCHIVADO' and reg_actualizado.estado == 'ARCHIVADO':
                reg_actualizado.fecha_archivo = timezone.now().date()

            if reg_actualizado.estado == 'DESTRUIDO':
                if not reg_actualizado.observaciones:
                    messages.warning(request,
                                     "Debe especificar en las observaciones la evidencia o justificación de la destrucción del registro.")
                    return render(request, 'h_m22_control_registros/formulario.html',
                                  {'form': form, 'accion': 'Gestionar'})
                if not reg_actualizado.fecha_destruccion:
                    reg_actualizado.fecha_destruccion = timezone.now().date()

            reg_actualizado.save()
            messages.success(request, "Configuración del registro actualizada correctamente.")
            return redirect('m22_dashboard')
    else:
        form = RegistroCalidadForm(instance=registro)

    return render(request, 'h_m22_control_registros/formulario.html', {'form': form, 'accion': 'Gestionar'})