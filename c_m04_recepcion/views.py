from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from .models import RecepcionMuestra, HistorialManejo
from .forms import RecepcionForm
from c_m03_muestreo.models import Muestra


@login_required
def dashboard_recepcion(request):
    # Límite crítico de tiempo: 24 horas en espera (puedes ajustar este número)
    limite_tiempo = timezone.now() - timedelta(hours=24)

    # Muestras registradas que NO han sido recibidas
    pendientes = Muestra.objects.filter(recepcion__isnull=True, activo=True).order_by('fecha_muestreo')

    # Evaluamos cada muestra pendiente para ver si cruzó el límite de tiempo
    for m in pendientes:
        if m.fecha_muestreo < limite_tiempo:
            m.alerta_retraso = True
        else:
            m.alerta_retraso = False

    # Muestras ya en proceso de laboratorio
    en_laboratorio = RecepcionMuestra.objects.all().select_related('muestra').order_by('-fecha_recepcion')

    return render(request, 'c_m04_recepcion/dashboard.html', {
        'pendientes': pendientes,
        'en_laboratorio': en_laboratorio
    })


@login_required
def registrar_entrada(request, muestra_id):
    muestra = get_object_or_404(Muestra, id=muestra_id)
    if request.method == 'POST':
        form = RecepcionForm(request.POST)
        if form.is_valid():
            recepcion = form.save(commit=False)
            recepcion.muestra = muestra
            recepcion.usuario_recepcion = request.user
            recepcion.save()

            # Registro inicial en historial
            HistorialManejo.objects.create(
                recepcion=recepcion,
                accion="Ingreso inicial al laboratorio",
                usuario=request.user
            )

            messages.success(request, f"Muestra {muestra.codigo} recibida correctamente.")
            return redirect('c_m04_dashboard')
    else:
        form = RecepcionForm()
    return render(request, 'c_m04_recepcion/form_recepcion.html', {'form': form, 'muestra': muestra})