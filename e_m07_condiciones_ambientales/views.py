from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import RegistroAmbiental, AreaLaboratorio
from .forms import RegistroAmbientalForm


@login_required
def dashboard_condiciones(request):
    # Traemos los últimos 50 registros para el panel principal
    registros = RegistroAmbiental.objects.all()[:50]
    areas = AreaLaboratorio.objects.all()

    return render(request, 'e_m07_condiciones_ambientales/dashboard.html', {
        'registros': registros,
        'areas': areas
    })


@login_required
def crear_registro_ambiental(request):
    if request.method == 'POST':
        form = RegistroAmbientalForm(request.POST)
        if form.is_valid():
            registro = form.save(commit=False)
            registro.registrado_por = request.user  # Trazabilidad Obligatoria
            registro.save()
            return redirect('e_m07_dashboard')
    else:
        form = RegistroAmbientalForm()

    return render(request, 'e_m07_condiciones_ambientales/formulario.html', {'form': form})