from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from .models import MaterialReferencia, UsoMaterial
from .forms import MaterialReferenciaForm, UsoMaterialForm


@login_required
def dashboard_trazabilidad(request):
    hoy = timezone.now().date()
    limite_alerta = hoy + timedelta(days=30)

    materiales = MaterialReferencia.objects.filter(activo=True).order_by('fecha_caducidad')

    for m in materiales:
        if m.estado == 'AGOTADO':
            m.alerta = 'OK'
        elif m.fecha_caducidad < hoy:
            m.alerta = 'CRITICA'  # Caducado
            if m.estado == 'VIGENTE':
                m.estado = 'CADUCADO'  # Auto-actualización de estado
                m.save()
        elif m.fecha_caducidad <= limite_alerta:
            m.alerta = 'PREVENTIVA'  # Próximo a caducar
        else:
            m.alerta = 'OK'

    return render(request, 'd_m09_trazabilidad/dashboard.html', {'materiales': materiales})


@login_required
def nuevo_mrc(request):
    if request.method == 'POST':
        form = MaterialReferenciaForm(request.POST, request.FILES)
        if form.is_valid():
            mrc = form.save(commit=False)
            mrc.usuario_creacion = request.user
            mrc.save()
            messages.success(request, 'Material de Referencia inventariado exitosamente.')
            return redirect('d_m09_dashboard')
    else:
        form = MaterialReferenciaForm()
    return render(request, 'd_m09_trazabilidad/form_mrc.html', {'form': form, 'titulo': 'Alta de Nuevo MRC'})


@login_required
def detalle_mrc(request, mrc_id):
    mrc = get_object_or_404(MaterialReferencia, id=mrc_id)
    usos = mrc.usos.all().order_by('-fecha_uso')

    if request.method == 'POST':
        form = UsoMaterialForm(request.POST)
        if form.is_valid():
            uso = form.save(commit=False)
            uso.material = mrc
            uso.usuario_registro = request.user
            uso.save()
            messages.success(request, 'Registro de uso guardado correctamente para trazabilidad.')
            return redirect('d_m09_detalle', mrc_id=mrc.id)
    else:
        form = UsoMaterialForm()

    return render(request, 'd_m09_trazabilidad/detalle.html', {
        'mrc': mrc,
        'usos': usos,
        'form': form
    })