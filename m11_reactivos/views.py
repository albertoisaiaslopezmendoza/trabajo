from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Reactivo, Proveedor, LoteReactivo, ServicioExterno
from .forms import ReactivoForm, LoteReactivoForm

def dashboard(request):
    reactivos_count = Reactivo.objects.count()
    proveedores_count = Proveedor.objects.filter(aprobado=True).count()
    lotes_count = LoteReactivo.objects.count()
    servicios_count = ServicioExterno.objects.count()

    context = {
        'reactivos_count': reactivos_count,
        'proveedores_count': proveedores_count,
        'lotes_count': lotes_count,
        'servicios_count': servicios_count,
    }
    return render(request, 'm11_reactivos/dashboard.html', context)


def lista_reactivos(request):
    """Muestra el catálogo de reactivos."""
    reactivos = Reactivo.objects.all().select_related('proveedor')
    return render(request, 'm11_reactivos/lista_reactivos.html', {'reactivos': reactivos})


def nuevo_reactivo(request):
    """Procesa el formulario para crear un nuevo reactivo."""
    if request.method == 'POST':
        form = ReactivoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reactivo registrado exitosamente.')
            return redirect('m11_lista_reactivos')
    else:
        form = ReactivoForm()

    return render(request, 'm11_reactivos/formulario.html', {
        'form': form,
        'titulo': 'Nuevo Reactivo'
    })


def lista_lotes(request):
    """Muestra el inventario de lotes recibidos."""
    lotes = LoteReactivo.objects.all().select_related('reactivo')
    return render(request, 'm11_reactivos/lista_lotes.html', {'lotes': lotes})


def nuevo_lote(request):
    """Procesa el formulario para registrar la entrada de un nuevo lote."""
    if request.method == 'POST':
        form = LoteReactivoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Lote registrado exitosamente.')
            return redirect('m11_lista_lotes')
    else:
        form = LoteReactivoForm()

    return render(request, 'm11_reactivos/formulario.html', {
        'form': form,
        'titulo': 'Registrar Nuevo Lote'
    })