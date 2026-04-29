from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import RiesgoOportunidad
from .forms import RiesgoOportunidadForm


@login_required
def dashboard(request):
    ros = RiesgoOportunidad.objects.all().order_by('-fecha_actualizacion')
    return render(request, 'g_m19_riesgos_oportunidades/dashboard.html', {'ros': ros})


@login_required
def crear_ro(request):
    if request.method == 'POST':
        form = RiesgoOportunidadForm(request.POST)
        if form.is_valid():
            ro = form.save(commit=False)
            ro.identificado_por = request.user
            ro.save()
            messages.success(request, "Riesgo / Oportunidad registrado exitosamente.")
            return redirect('m19_dashboard')
    else:
        form = RiesgoOportunidadForm()
    return render(request, 'g_m19_riesgos_oportunidades/formulario.html', {'form': form, 'accion': 'Registrar'})


@login_required
def editar_ro(request, pk):
    ro = get_object_or_404(RiesgoOportunidad, pk=pk)

    # Bloqueo por trazabilidad ISO 17025
    if ro.estado == 'CERRADO':
        messages.error(request, "Registro CERRADO. No admite modificaciones.")
        return redirect('m19_dashboard')

    if request.method == 'POST':
        form = RiesgoOportunidadForm(request.POST, instance=ro)
        if form.is_valid():
            ro_actualizado = form.save(commit=False)

            # Validación Cláusula 8.5.3: Si se cierra, debe tener evaluación de eficacia
            if ro_actualizado.estado == 'CERRADO':
                if not ro_actualizado.evaluacion_eficacia:
                    messages.warning(request, "Para cerrar el registro, debe detallar la evaluación de eficacia.")
                    return render(request, 'g_m19_riesgos_oportunidades/formulario.html',
                                  {'form': form, 'accion': 'Evaluar'})

                # Sello de fecha de cierre
                if not ro_actualizado.fecha_cierre:
                    ro_actualizado.fecha_cierre = timezone.now()

            ro_actualizado.save()
            messages.success(request, "Registro actualizado correctamente.")
            return redirect('m19_dashboard')
    else:
        form = RiesgoOportunidadForm(instance=ro)

    return render(request, 'g_m19_riesgos_oportunidades/formulario.html', {'form': form, 'accion': 'Gestionar'})