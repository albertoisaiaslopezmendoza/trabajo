from django.shortcuts import render, redirect
from .models import DocumentoControlado
from .forms import DocumentoForm

def dashboard(request):
    # Recuperamos todos los documentos de la base de datos
    documentos = DocumentoControlado.objects.all()
    # Pasamos los documentos al template html
    return render(request, 'm05_control_documental/mapa.html', {'documentos': documentos})

def crear_documento(request):
    # Si la petición es POST, el usuario está enviando datos para guardar
    if request.method == 'POST':
        form = DocumentoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('m05_control_documental:dashboard')
    else:
        # Si no es POST, mostramos el formulario vacío
        form = DocumentoForm()

    return render(request, 'm05_control_documental/form.html', {'form': form})