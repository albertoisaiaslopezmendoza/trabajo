from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required  # Requisito LABCOR: Control de acceso
from .models import Reactivo, Proveedor, LoteReactivo, ServicioExterno
from .forms import ReactivoForm, LoteReactivoForm, ProveedorForm, ServicioExternoForm


@login_required
def dashboard(request):
    context = {
        'reactivos_count': Reactivo.objects.filter(activo=True).count(),
        'proveedores_count': Proveedor.objects.filter(aprobado=True, activo=True).count(),
        'lotes_count': LoteReactivo.objects.filter(activo=True).count(),
        'servicios_count': ServicioExterno.objects.filter(activo=True).count(),
    }
    return render(request, 'm11_reactivos/dashboard.html', context)


@login_required
def lista_reactivos(request):
    reactivos = Reactivo.objects.filter(activo=True).select_related('proveedor')
    return render(request, 'm11_reactivos/lista_reactivos.html', {'reactivos': reactivos})


@login_required
def nuevo_reactivo(request):
    if request.method == 'POST':
        form = ReactivoForm(request.POST, request.FILES)
        if form.is_valid():
            reactivo = form.save(commit=False)

            nombre_prov = form.cleaned_data.get('nombre_proveedor')
            if nombre_prov:
                proveedor, created = Proveedor.objects.get_or_create(
                    nombre=nombre_prov,
                    defaults={'usuario_creacion': request.user}
                )
                reactivo.proveedor = proveedor

            reactivo.usuario_creacion = request.user
            reactivo.save()
            messages.success(request, 'Reactivo registrado exitosamente.')
            return redirect('m11_lista_reactivos')
    else:
        form = ReactivoForm()

    proveedores = Proveedor.objects.filter(activo=True)
    return render(request, 'm11_reactivos/formulario.html', {
        'form': form,
        'titulo': 'Nuevo Reactivo',
        'proveedores': proveedores
    })


@login_required
def lista_lotes(request):
    lotes = LoteReactivo.objects.filter(activo=True).select_related('reactivo')
    return render(request, 'm11_reactivos/lista_lotes.html', {'lotes': lotes})


@login_required
def nuevo_lote(request):
    if request.method == 'POST':
        form = LoteReactivoForm(request.POST, request.FILES)
        if form.is_valid():
            lote = form.save(commit=False)
            lote.usuario_creacion = request.user
            lote.save()
            messages.success(request, 'Lote registrado exitosamente.')
            return redirect('m11_lista_lotes')
    else:
        form = LoteReactivoForm()

    return render(request, 'm11_reactivos/formulario.html', {
        'form': form,
        'titulo': 'Registrar Nuevo Lote'
    })


# --- VISTAS: PROVEEDORES (ISO 17025: 6.6) ---

@login_required
def lista_proveedores(request):
    """Muestra el catálogo de proveedores."""
    proveedores = Proveedor.objects.filter(activo=True)
    return render(request, 'm11_reactivos/lista_proveedores.html', {'proveedores': proveedores})


@login_required
def nuevo_proveedor(request):
    """Procesa el formulario para registrar un nuevo proveedor garantizando el Audit Trail."""
    if request.method == 'POST':
        form = ProveedorForm(request.POST)
        if form.is_valid():
            prov = form.save(commit=False)
            prov.usuario_creacion = request.user # Cumplimiento de Audit Trail
            prov.save()
            messages.success(request, 'Proveedor registrado exitosamente.')
            return redirect('m11_lista_proveedores')
    else:
        form = ProveedorForm()
    return render(request, 'm11_reactivos/formulario.html', {'form': form, 'titulo': 'Nuevo Proveedor'})


# --- VISTAS: SERVICIOS EXTERNOS (ISO 17025: 6.6) ---

@login_required
def lista_servicios(request):
    """Muestra el historial de servicios externos."""
    servicios = ServicioExterno.objects.filter(activo=True).select_related('proveedor')
    return render(request, 'm11_reactivos/lista_servicios.html', {'servicios': servicios})


@login_required
def nuevo_servicio(request):
    """Procesa el formulario para registrar un servicio externo garantizando el Audit Trail."""
    if request.method == 'POST':
        form = ServicioExternoForm(request.POST, request.FILES)
        if form.is_valid():
            servicio = form.save(commit=False)
            servicio.usuario_creacion = request.user # Cumplimiento de Audit Trail
            servicio.save()
            messages.success(request, 'Servicio registrado exitosamente.')
            return redirect('m11_lista_servicios')
    else:
        form = ServicioExternoForm()
    return render(request, 'm11_reactivos/formulario.html', {'form': form, 'titulo': 'Nuevo Servicio Externo'})