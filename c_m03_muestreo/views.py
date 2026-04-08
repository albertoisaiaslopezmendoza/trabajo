from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Muestra, CadenaCustodia
from .forms import MuestraForm, CadenaCustodiaForm


@login_required
def dashboard_muestreo(request):
    muestras = Muestra.objects.filter(activo=True).order_by('-fecha_creacion')
    return render(request, 'c_m03_muestreo/dashboard.html', {'muestras': muestras})


@login_required
def nueva_muestra(request):
    if request.method == 'POST':
        form = MuestraForm(request.POST)
        if form.is_valid():
            muestra = form.save(commit=False)
            muestra.usuario_creacion = request.user  # Control Audit Trail
            muestra.save()
            messages.success(request, 'Muestra registrada exitosamente (ISO 17025: 7.3).')
            return redirect('c_m03_dashboard')
    else:
        form = MuestraForm()
    return render(request, 'c_m03_muestreo/form_muestra.html', {'form': form, 'titulo': 'Registro de Muestreo'})


@login_required
def detalle_custodia(request, muestra_id):
    muestra = get_object_or_404(Muestra, id=muestra_id)
    custodias = muestra.custodias.all().order_by('-fecha_transferencia')

    if request.method == 'POST':
        form = CadenaCustodiaForm(request.POST)
        if form.is_valid():
            custodia = form.save(commit=False)
            custodia.muestra = muestra
            custodia.usuario_creacion = request.user
            custodia.save()
            messages.success(request, 'Transferencia registrada en Cadena de Custodia.')
            return redirect('c_m03_custodia', muestra_id=muestra.id)
    else:
        form = CadenaCustodiaForm()

    return render(request, 'c_m03_muestreo/custodia.html', {'muestra': muestra, 'custodias': custodias, 'form': form})