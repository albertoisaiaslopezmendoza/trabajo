# b_m17_gestion_quejas/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Queja, InvestigacionQueja
from .forms import QuejaForm, InvestigacionForm


@login_required
def dashboard_quejas(request):
    quejas = Queja.objects.all().order_by('-fecha_registro')
    return render(request, 'b_m17_gestion_quejas/dashboard.html', {'quejas': quejas})


@login_required
def registrar_queja(request):
    if request.method == 'POST':
        form = QuejaForm(request.POST)
        if form.is_valid():
            queja = form.save(commit=False)
            queja.recibida_por = request.user
            queja.save()
            messages.success(request, "Queja registrada correctamente.")
            return redirect('b_m17_gestion_quejas:dashboard')
    else:
        form = QuejaForm()
    return render(request, 'b_m17_gestion_quejas/form_queja.html', {'form': form})


@login_required
def investigar_queja(request, queja_id):
    queja = get_object_or_404(Queja, id=queja_id)

    # Buscamos si ya existe una investigación
    try:
        investigacion = InvestigacionQueja.objects.get(queja=queja)
    except InvestigacionQueja.DoesNotExist:
        # Si no existe, dejamos la instancia en None para que el formulario nazca vacío
        investigacion = None

    if request.method == 'POST':
        # Si la investigación ya existe, la actualiza. Si era None, crea una nueva.
        form = InvestigacionForm(request.POST, instance=investigacion)
        if form.is_valid():
            inv = form.save(commit=False)
            inv.queja = queja  # Aseguramos de enlazarla con la queja
            inv.responsable = request.user
            inv.save()

            # Actualizar el estado de la queja
            queja.estado = 'RESUELTA'
            if inv.notificacion_enviada:
                queja.estado = 'CERRADA'
            queja.save()

            messages.success(request, f"Investigación para {queja.folio} guardada exitosamente.")
            return redirect('b_m17_gestion_quejas:dashboard')
    else:
        # Se muestra el formulario (con datos si ya existía la investigación, o vacío si no)
        form = InvestigacionForm(instance=investigacion)

    return render(request, 'b_m17_gestion_quejas/form_investigacion.html', {'form': form, 'queja': queja})