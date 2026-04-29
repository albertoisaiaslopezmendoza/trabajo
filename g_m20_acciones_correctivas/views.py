from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import AccionCorrectiva
from .forms import AccionCorrectivaForm


@login_required
def dashboard(request):
    acciones = AccionCorrectiva.objects.all().order_by('-fecha_apertura')
    return render(request, 'g_m20_acciones_correctivas/dashboard.html', {'acciones': acciones})


@login_required
def crear_ac(request):
    if request.method == 'POST':
        form = AccionCorrectivaForm(request.POST)
        if form.is_valid():
            ac = form.save(commit=False)
            ac.reportado_por = request.user
            ac.save()
            messages.success(request, "Acción Correctiva registrada exitosamente.")
            return redirect('m20_dashboard')
    else:
        form = AccionCorrectivaForm()
    return render(request, 'g_m20_acciones_correctivas/formulario.html', {'form': form, 'accion': 'Registrar'})


@login_required
def editar_ac(request, pk):
    ac = get_object_or_404(AccionCorrectiva, pk=pk)

    # Bloqueo de trazabilidad: Una AC cerrada no se puede modificar
    if ac.estado == 'CERRADA':
        messages.error(request,
                       "Esta Acción Correctiva ya se encuentra CERRADA. Por motivos de auditoría, no admite modificaciones.")
        return redirect('m20_dashboard')

    if request.method == 'POST':
        form = AccionCorrectivaForm(request.POST, instance=ac)
        if form.is_valid():
            ac_actualizada = form.save(commit=False)

            # Validación ISO 17025 Cláusula 8.7.1 d): Obligar análisis de causa y eficacia antes de cerrar
            if ac_actualizada.estado == 'CERRADA':
                errores = []
                if not ac_actualizada.analisis_causa_raiz:
                    errores.append("Debe detallar el Análisis de Causa Raíz.")
                if not ac_actualizada.evaluacion_eficacia:
                    errores.append("Debe detallar la Evaluación de Eficacia.")
                if not ac_actualizada.es_eficaz:
                    errores.append(
                        "No puede cerrar la Acción Correctiva si no es eficaz. (Regrese a fase de implementación).")

                if errores:
                    for error in errores:
                        messages.warning(request, error)
                    return render(request, 'g_m20_acciones_correctivas/formulario.html',
                                  {'form': form, 'accion': 'Editar / Evaluar'})

                # Si pasa las validaciones, sella la fecha de cierre
                if not ac_actualizada.fecha_cierre:
                    ac_actualizada.fecha_cierre = timezone.now()

            ac_actualizada.save()
            messages.success(request, "Acción Correctiva actualizada correctamente.")
            return redirect('m20_dashboard')
    else:
        form = AccionCorrectivaForm(instance=ac)

    return render(request, 'g_m20_acciones_correctivas/formulario.html', {'form': form, 'accion': 'Editar / Gestionar'})