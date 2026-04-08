from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Equipo, Mantenimiento, Calibracion
from .forms import EquipoForm, MantenimientoForm


@login_required
def dashboard_equipos(request):
    """Muestra el panel principal con el inventario y las alertas dinámicas."""
    hoy = timezone.now().date()
    equipos = Equipo.objects.filter(activo=True).order_by('codigo_interno')

    for eq in equipos:
        # Lógica de Alertas ISO 17025
        ultima_cal = eq.calibraciones.order_by('-proxima_calibracion').first()
        ultimo_mant = eq.mantenimientos.order_by('-proximo_mantenimiento').first()

        eq.calibracion_vencida = ultima_cal and ultima_cal.proxima_calibracion <= hoy
        eq.mantenimiento_vencido = ultimo_mant and ultimo_mant.proximo_mantenimiento <= hoy
        eq.alerta_critica = eq.calibracion_vencida or eq.mantenimiento_vencido

    return render(request, 'd_m08_equipos/dashboard.html', {
        'equipos': equipos,
        'hoy': hoy
    })


@login_required
def nuevo_equipo(request):
    """Procesa el formulario para dar de alta un equipo nuevo en el inventario."""
    if request.method == 'POST':
        form = EquipoForm(request.POST)
        if form.is_valid():
            equipo = form.save(commit=False)
            equipo.usuario_creacion = request.user
            equipo.save()
            messages.success(request, 'Equipo inventariado correctamente.')
            return redirect('d_m08_dashboard')
    else:
        form = EquipoForm()
    return render(request, 'd_m08_equipos/formulario.html', {'form': form, 'titulo': 'Registro de Equipo'})


@login_required
def detalle_equipo(request, equipo_id):
    """Muestra el historial completo de calibraciones y mantenimientos de un equipo específico."""
    equipo = get_object_or_404(Equipo, id=equipo_id)

    # Traemos el historial ordenado desde el más reciente al más antiguo
    mantenimientos = equipo.mantenimientos.all().order_by('-fecha_servicio')
    calibraciones = equipo.calibraciones.all().order_by('-fecha_calibracion')

    return render(request, 'd_m08_equipos/detalle.html', {
        'equipo': equipo,
        'mantenimientos': mantenimientos,
        'calibraciones': calibraciones
    })