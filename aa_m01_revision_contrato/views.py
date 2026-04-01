from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import RevisionContrato
from .forms import RevisionContratoForm
from django.utils import timezone

@login_required
def lista_contratos(request):
    contratos = RevisionContrato.objects.all().order_by('-fecha_solicitud')
    return render(request, 'aa_m01_revision_contrato/lista.html', {'contratos': contratos})

@login_required
def crear_contrato(request):
    if request.method == 'POST':
        form = RevisionContratoForm(request.POST)
        if form.is_valid():
            contrato = form.save(commit=False)
            contrato.revisado_por = request.user
            if contrato.estado != 'PENDIENTE':
                contrato.fecha_revision = timezone.now()
            contrato.save()
            return redirect('aa_m01_revision_contrato:lista')
    else:
        form = RevisionContratoForm()
    return render(request, 'aa_m01_revision_contrato/form.html', {'form': form, 'titulo': 'Nueva Revisión de Contrato'})

@login_required
def editar_contrato(request, pk):
    contrato = get_object_or_404(RevisionContrato, pk=pk)
    if request.method == 'POST':
        form = RevisionContratoForm(request.POST, instance=contrato)
        if form.is_valid():
            contrato = form.save(commit=False)
            contrato.revisado_por = request.user
            contrato.fecha_revision = timezone.now()
            contrato.save()
            return redirect('aa_m01_revision_contrato:lista')
    else:
        form = RevisionContratoForm(instance=contrato)
    return render(request, 'aa_m01_revision_contrato/form.html', {'form': form, 'titulo': 'Editar Revisión'})