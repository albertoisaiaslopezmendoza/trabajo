from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import TrabajoNoConforme
from .forms import TrabajoNoConformeForm


@login_required
def dashboard(request):
    tncs = TrabajoNoConforme.objects.all().order_by('-fecha_identificacion')
    return render(request, 'g_m18_trabajo_no_conforme/dashboard.html', {'tncs': tncs})


@login_required
def crear_tnc(request):
    if request.method == 'POST':
        form = TrabajoNoConformeForm(request.POST)
        if form.is_valid():
            tnc = form.save(commit=False)
            tnc.identificado_por = request.user
            tnc.save()
            messages.success(request, "Trabajo No Conforme registrado exitosamente.")
            return redirect('m18_dashboard')
    else:
        form = TrabajoNoConformeForm()
    return render(request, 'g_m18_trabajo_no_conforme/formulario.html', {'form': form, 'accion': 'Registrar'})


@login_required
def editar_tnc(request, pk):
    tnc = get_object_or_404(TrabajoNoConforme, pk=pk)

    # BLOQUEO: Si está cerrado, no se puede editar por trazabilidad
    if tnc.estado == 'CERRADO':
        messages.error(request, "Este Trabajo No Conforme ya se encuentra cerrado. No admite modificaciones.")
        return redirect('m18_dashboard')

    if request.method == 'POST':
        form = TrabajoNoConformeForm(request.POST, instance=tnc)
        if form.is_valid():
            tnc_actualizado = form.save(commit=False)

            # Validación ISO 17025: No cerrar si falta el autorizador de reanudación
            if tnc_actualizado.estado == 'CERRADO' and not tnc_actualizado.autoriza_reanudar:
                messages.warning(request, "Para cerrar el TNC, debe especificar quién autorizó reanudar el trabajo.")
            else:
                # Sello automático de fecha si hay alguien que autoriza y aún no hay fecha
                if tnc_actualizado.autoriza_reanudar and not tnc_actualizado.fecha_reanudacion:
                    tnc_actualizado.fecha_reanudacion = timezone.now()

                tnc_actualizado.save()
                messages.success(request, "Trabajo No Conforme actualizado correctamente.")
                return redirect('m18_dashboard')
    else:
        form = TrabajoNoConformeForm(instance=tnc)

    return render(request, 'g_m18_trabajo_no_conforme/formulario.html', {'form': form, 'accion': 'Editar / Evaluar'})