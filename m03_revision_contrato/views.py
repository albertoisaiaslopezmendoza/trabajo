from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import RevisionContrato, Cotizacion
from .forms import RevisionForm


@login_required
def dashboard_m03(request):
    # Tabla histórica (equivalente a _view en el original)
    revisiones = RevisionContrato.objects.all()[:50]
    return render(request, 'm03_revision_contrato/dashboard.html', {'revisiones': revisiones})


@login_required
def crear_revision(request):
    if request.method == 'POST':
        form = RevisionForm(request.POST)
        if form.is_valid():
            revision = form.save(commit=False)

            # Obtener datos snapshot de la cotización seleccionada
            cotizacion = form.cleaned_data['cotizacion']
            revision.cliente = cotizacion.cliente
            revision.ensayo = cotizacion.ensayo
            revision.norma = cotizacion.norma

            # Usuario actual
            revision.aprobado_por = request.user.username
            if revision.estado == 'APROBADO':
                revision.aprobado = True

            revision.save()
            messages.success(request, "Revisión registrada correctamente.")
            return redirect('m03_dashboard')
        else:
            messages.error(request, "Error en el formulario. Verifique los campos.")
    else:
        form = RevisionForm()

    return render(request, 'm03_revision_contrato/form.html', {'form': form})


# API simple para obtener datos de la cotización vía AJAX (para llenar inputs readonly)
from django.http import JsonResponse


@login_required
def api_cotizacion_info(request, cotizacion_id):
    try:
        cot = Cotizacion.objects.get(id=cotizacion_id)
        return JsonResponse({
            'cliente': cot.cliente,
            'ensayo': cot.ensayo,
            'norma': cot.norma
        })
    except Cotizacion.DoesNotExist:
        return JsonResponse({'error': 'No encontrado'}, status=404)