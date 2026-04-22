from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import RegistroQC
from .forms import RegistroQCForm

@login_required
def dashboard_qc(request):
    controles = RegistroQC.objects.all()
    return render(request, 'e_m14_aseguramiento_validez/dashboard.html', {'controles': controles})

@login_required
def crear_editar_qc(request, qc_id=None):
    control = None
    es_lectura = False

    if qc_id:
        control = get_object_or_404(RegistroQC, id=qc_id)
        # Rúbrica: Bloqueo de edición de registros finalizados
        if control.estado == 'FINALIZADO':
            es_lectura = True

    if request.method == 'POST':
        if es_lectura:
            messages.error(request, "Acceso Denegado: Este registro de Control de Calidad está finalizado y es inmutable.")
            return redirect('e_m14_dashboard')

        form = RegistroQCForm(request.POST, request.FILES, instance=control)
        if form.is_valid():
            reg = form.save(commit=False)
            if not qc_id: # Audit trail: asentar quién lo ejecutó
                reg.analista = request.user
            reg.save()
            messages.success(request, "Registro de Aseguramiento de Validez guardado correctamente.")
            return redirect('e_m14_dashboard')
    else:
        form = RegistroQCForm(instance=control)

    return render(request, 'e_m14_aseguramiento_validez/formulario.html', {
        'form': form,
        'control': control,
        'es_lectura': es_lectura
    })