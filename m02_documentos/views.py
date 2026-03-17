from django.shortcuts import render, redirect, get_object_or_404
from django.http import FileResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Documento
from .forms import DocumentoForm, CambioFormSet, DistribucionFormSet
from .utils import generar_pdf_documento


@login_required
def documento_list(request):
    docs = Documento.objects.all()
    query = request.GET.get('q')
    if query:
        docs = docs.filter(titulo__icontains=query) | docs.filter(codigo__icontains=query)
    return render(request, 'm02_documentos/lista.html', {'documentos': docs})


@login_required
def documento_create(request):
    if request.method == 'POST':
        form = DocumentoForm(request.POST)
        form_cambios = CambioFormSet(request.POST)
        form_dist = DistribucionFormSet(request.POST)

        if form.is_valid() and form_cambios.is_valid() and form_dist.is_valid():
            doc = form.save()
            form_cambios.instance = doc
            form_cambios.save()
            form_dist.instance = doc
            form_dist.save()
            messages.success(request, 'Documento creado correctamente.')
            return redirect('m02_documentos:lista')
    else:
        form = DocumentoForm()
        form_cambios = CambioFormSet()
        form_dist = DistribucionFormSet()

    return render(request, 'm02_documentos/form.html', {
        'form': form,
        'form_cambios': form_cambios,
        'form_dist': form_dist,
        'title': 'Nuevo Documento'
    })


@login_required
def documento_update(request, pk):
    doc = get_object_or_404(Documento, pk=pk)
    if request.method == 'POST':
        form = DocumentoForm(request.POST, instance=doc)
        form_cambios = CambioFormSet(request.POST, instance=doc)
        form_dist = DistribucionFormSet(request.POST, instance=doc)

        if form.is_valid() and form_cambios.is_valid() and form_dist.is_valid():
            form.save()
            form_cambios.save()
            form_dist.save()
            messages.success(request, 'Documento actualizado.')
            return redirect('m02_documentos:lista')
    else:
        form = DocumentoForm(instance=doc)
        form_cambios = CambioFormSet(instance=doc)
        form_dist = DistribucionFormSet(instance=doc)

    return render(request, 'm02_documentos/form.html', {
        'form': form,
        'form_cambios': form_cambios,
        'form_dist': form_dist,
        'title': f'Editar {doc.codigo}'
    })


@login_required
def documento_pdf(request, pk):
    doc = get_object_or_404(Documento, pk=pk)
    buffer = generar_pdf_documento(doc)
    return FileResponse(buffer, as_attachment=False, filename=f'{doc.codigo}.pdf')