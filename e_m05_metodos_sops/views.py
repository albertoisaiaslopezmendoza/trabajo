from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import MetodoSOP
from .forms import MetodoSOPForm


@login_required
def dashboard_metodos(request):
    # Los técnicos solo deberían usar los Vigentes
    metodos = MetodoSOP.objects.all()
    return render(request, 'e_m05_metodos_sops/dashboard.html', {'metodos': metodos})


@login_required
def crear_metodo(request):
    # Aquí puedes añadir un decorador o if para verificar que sea Gestor de Calidad o Director
    if request.method == 'POST':
        form = MetodoSOPForm(request.POST, request.FILES)
        if form.is_valid():
            metodo = form.save(commit=False)
            metodo.creado_por = request.user  # Trazabilidad obligatoria
            metodo.save()
            return redirect('e_m05_dashboard')
    else:
        form = MetodoSOPForm()

    return render(request, 'e_m05_metodos_sops/formulario.html', {'form': form, 'accion': 'Crear'})