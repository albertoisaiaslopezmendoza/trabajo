# h_m23_auditorias_internas/views.py
from django.shortcuts import render, redirect
from .models import InternalAudit, AuditFinding
from .forms import InternalAuditForm, AuditFindingForm


def dashboard_auditorias(request):
    """Muestra la lista de auditorías y permite crear nuevas."""
    auditorias = InternalAudit.objects.all().order_by('-id')
    hallazgos = AuditFinding.objects.all().order_by('-id')

    if request.method == 'POST':
        if 'btn_audit' in request.POST:
            audit_form = InternalAuditForm(request.POST)
            finding_form = AuditFindingForm()
            if audit_form.is_valid():
                audit_form.save()
                return redirect('m23_dashboard')
        elif 'btn_finding' in request.POST:
            finding_form = AuditFindingForm(request.POST)
            audit_form = InternalAuditForm()
            if finding_form.is_valid():
                finding_form.save()
                return redirect('m23_dashboard')
    else:
        audit_form = InternalAuditForm()
        finding_form = AuditFindingForm()

    context = {
        'auditorias': auditorias,
        'hallazgos': hallazgos,
        'audit_form': audit_form,
        'finding_form': finding_form,
    }
    return render(request, 'h_m23_auditorias_internas/dashboard.html', context)