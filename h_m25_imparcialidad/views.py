# h_m25_imparcialidad/views.py
from django.shortcuts import render, redirect
from .models import DeclaracionImparcialidad, ConflictoInteres, Mitigacion
from .forms import DeclaracionForm, ConflictoForm, MitigacionForm


def dashboard_imparcialidad(request):
    """Muestra el panel de Imparcialidad y procesa la creación de registros."""
    declaraciones = DeclaracionImparcialidad.objects.all().order_by('-fecha_declaracion')
    conflictos = ConflictoInteres.objects.all().order_by('-fecha_reporte')
    mitigaciones = Mitigacion.objects.all().order_by('-fecha_implementacion')

    if request.method == 'POST':
        # Detectar qué formulario se envió usando el nombre del botón
        if 'btn_declaracion' in request.POST:
            form_dec = DeclaracionForm(request.POST)
            if form_dec.is_valid():
                form_dec.save()
                return redirect('m25_dashboard')

        elif 'btn_conflicto' in request.POST:
            form_conf = ConflictoForm(request.POST)
            if form_conf.is_valid():
                form_conf.save()
                return redirect('m25_dashboard')

        elif 'btn_mitigacion' in request.POST:
            form_mit = MitigacionForm(request.POST)
            if form_mit.is_valid():
                form_mit.save()
                return redirect('m25_dashboard')

    # Si no es POST, instanciamos formularios vacíos
    form_dec = DeclaracionForm()
    form_conf = ConflictoForm()
    form_mit = MitigacionForm()

    context = {
        'declaraciones': declaraciones,
        'conflictos': conflictos,
        'mitigaciones': mitigaciones,
        'form_dec': form_dec,
        'form_conf': form_conf,
        'form_mit': form_mit,
    }
    return render(request, 'h_m25_imparcialidad/dashboard.html', context)