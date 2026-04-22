from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CalculoIncertidumbre, PresupuestoIncertidumbre
from .forms import CalculoIncertidumbreForm

@login_required
def dashboard_calculos(request):
    calculos = CalculoIncertidumbre.objects.all().select_related('registro_tecnico', 'presupuesto_utilizado')
    presupuestos = PresupuestoIncertidumbre.objects.filter(es_vigente=True)
    return render(request, 'e_m13_calculos_incertidumbre/dashboard.html', {
        'calculos': calculos,
        'presupuestos': presupuestos
    })

@login_required
def registrar_calculo(request):
    if request.method == 'POST':
        form = CalculoIncertidumbreForm(request.POST)
        if form.is_valid():
            calc = form.save(commit=False)
            calc.calculado_por = request.user # Trazabilidad
            # Validar que el RT esté finalizado antes de anexar la incertidumbre
            if calc.registro_tecnico.estado != 'FINALIZADO':
                messages.error(request, "Error: El Registro Técnico debe estar FINALIZADO para calcular su incertidumbre.")
            else:
                calc.save()
                messages.success(request, f"Incertidumbre calculada guardada con éxito (U = {calc.incertidumbre_expandida}). Registro Bloqueado.")
                return redirect('e_m13_dashboard')
    else:
        form = CalculoIncertidumbreForm()

    return render(request, 'e_m13_calculos_incertidumbre/formulario.html', {'form': form})