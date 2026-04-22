from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import RegistroTecnico
from .forms import RegistroTecnicoForm

@login_required
def dashboard_registros(request):
    registros = RegistroTecnico.objects.all()
    return render(request, 'e_m12_ejecucion_registros/dashboard.html', {'registros': registros})

@login_required
def crear_editar_registro(request, registro_id=None):
    registro = None
    es_lectura = False

    # Si se recibe un ID, estamos editando o consultando
    if registro_id:
        registro = get_object_or_404(RegistroTecnico, id=registro_id)
        # Rúbrica: Bloqueo de edición si ya está finalizado
        if registro.estado in ['FINALIZADO', 'REVISADO']:
            es_lectura = True

    if request.method == 'POST':
        # Validar seguridad backend: evitar POST si está bloqueado
        if es_lectura:
            messages.error(request, "Violación ISO 17025: El registro está bloqueado y no puede modificarse.")
            return redirect('e_m12_dashboard')

        form = RegistroTecnicoForm(request.POST, request.FILES, instance=registro)
        if form.is_valid():
            reg = form.save(commit=False)
            if not registro_id: # Asignación de analista en creación (Audit Trail)
                reg.analista = request.user
            reg.save()
            messages.success(request, "Registro Técnico actualizado exitosamente.")
            return redirect('e_m12_dashboard')
    else:
        form = RegistroTecnicoForm(instance=registro)

    return render(request, 'e_m12_ejecucion_registros/formulario.html', {
        'form': form,
        'registro': registro,
        'es_lectura': es_lectura
    })