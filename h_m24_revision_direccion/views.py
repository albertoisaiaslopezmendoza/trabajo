# h_m24_revision_direccion/views.py
from django.shortcuts import render, redirect
from .models import KPI, RevisionDireccion, AcuerdoRMD
from .forms import RevisionDireccionForm, AcuerdoRMDForm

def dashboard_revision(request):
    """Controla el tablero principal de Revisión por la Dirección."""
    kpis = KPI.objects.all()
    revisiones = RevisionDireccion.objects.all().order_by('-fecha_revision')
    acuerdos = AcuerdoRMD.objects.all().order_by('fecha_limite')

    if request.method == 'POST':
        if 'btn_revision' in request.POST:
            form_rev = RevisionDireccionForm(request.POST)
            form_acuerdo = AcuerdoRMDForm()
            if form_rev.is_valid():
                form_rev.save()
                return redirect('m24_dashboard')
        elif 'btn_acuerdo' in request.POST:
            form_acuerdo = AcuerdoRMDForm(request.POST)
            form_rev = RevisionDireccionForm()
            if form_acuerdo.is_valid():
                form_acuerdo.save()
                return redirect('m24_dashboard')
    else:
        form_rev = RevisionDireccionForm()
        form_acuerdo = AcuerdoRMDForm()

    context = {
        'kpis': kpis,
        'revisiones': revisiones,
        'acuerdos': acuerdos,
        'form_rev': form_rev,
        'form_acuerdo': form_acuerdo,
    }
    return render(request, 'h_m24_revision_direccion/dashboard.html', context)