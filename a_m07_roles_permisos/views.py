from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import PerfilPuesto, PerfilEmpleado
from .forms import PerfilPuestoForm, PerfilEmpleadoForm


@login_required
def lista_personal(request):
    empleados = PerfilEmpleado.objects.select_related('usuario', 'puesto').all()
    return render(request, 'a_m07_roles_permisos/lista_personal.html', {'empleados': empleados})


@login_required
def crear_personal(request):
    if request.method == 'POST':
        form = PerfilEmpleadoForm(request.POST, request.FILES)
        if form.is_valid():
            empleado = form.save(commit=False)

            # Obtenemos el texto ingresado por el usuario
            nombre_puesto_ingresado = form.cleaned_data.get('nombre_puesto')

            # Buscamos el puesto. Si no existe, lo creamos con valores "Por definir"
            puesto, created = PerfilPuesto.objects.get_or_create(
                nombre=nombre_puesto_ingresado,
                defaults={
                    'responsabilidades': 'Por definir',
                    'autoridades': 'Por definir',
                    'competencias_requeridas': 'Por definir'
                }
            )

            # Enlazamos el puesto al empleado y guardamos
            empleado.puesto = puesto
            empleado.save()
            return redirect('a_m07_roles_permisos:lista_personal')
    else:
        form = PerfilEmpleadoForm()

    # Enviamos los puestos a la plantilla para que funcione el autocompletado
    puestos = PerfilPuesto.objects.all()
    return render(request, 'a_m07_roles_permisos/form.html', {
        'form': form,
        'titulo': 'Asignar Puesto a Empleado',
        'puestos': puestos
    })


@login_required
def lista_puestos(request):
    puestos = PerfilPuesto.objects.all()
    return render(request, 'a_m07_roles_permisos/lista_puestos.html', {'puestos': puestos})


@login_required
def crear_puesto(request):
    if request.method == 'POST':
        form = PerfilPuestoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('a_m07_roles_permisos:lista_puestos')
    else:
        form = PerfilPuestoForm()
    return render(request, 'a_m07_roles_permisos/form.html', {'form': form, 'titulo': 'Nuevo Perfil de Puesto'})