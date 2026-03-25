# a03_mapa_procesos/views.py
from django.shortcuts import render

def dashboard(request):
    # Por ahora solo cargaremos la plantilla interactiva
    return render(request, 'a03_mapa_procesos/dashboard.html')