# b_m02_clientes/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cliente, AcuerdoConfidencialidad
from .forms import ClienteForm, AcuerdoConfidencialidadForm

@login_required
def dashboard_clientes(request):
    clientes = Cliente.objects.all().order_by('-fecha_registro')
    acuerdos = AcuerdoConfidencialidad.objects.all().order_by('-fecha_firma')
    return render(request, 'b_m02_clientes/dashboard.html', {
        'clientes': clientes,
        'acuerdos': acuerdos
    })

@login_required
def registrar_cliente(request):
    if request.method == 'POST':
        form = ClienteForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Cliente registrado exitosamente.")
            return redirect('b_m02_clientes:dashboard')
    else:
        form = ClienteForm()
    return render(request, 'b_m02_clientes/form_cliente.html', {'form': form})

@login_required
def registrar_acuerdo(request):
    if request.method == 'POST':
        form = AcuerdoConfidencialidadForm(request.POST, request.FILES)
        if form.is_valid():
            acuerdo = form.save(commit=False)
            acuerdo.registrado_por = request.user
            acuerdo.save()
            messages.success(request, "Acuerdo de confidencialidad registrado.")
            return redirect('b_m02_clientes:dashboard')
    else:
        form = AcuerdoConfidencialidadForm()
    return render(request, 'b_m02_clientes/form_acuerdo.html', {'form': form})