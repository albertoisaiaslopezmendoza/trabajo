# h_m23_auditorias_internas/forms.py
from django import forms
from .models import InternalAudit, AuditFinding

class InternalAuditForm(forms.ModelForm):
    class Meta:
        model = InternalAudit
        fields = ['audit_code', 'planned_date', 'performed_date', 'scope', 'lead_auditor', 'status']
        widgets = {
            'planned_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'performed_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'audit_code': forms.TextInput(attrs={'class': 'form-control'}),
            'scope': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'lead_auditor': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class AuditFindingForm(forms.ModelForm):
    class Meta:
        model = AuditFinding
        fields = ['audit', 'finding_type', 'description', 'severity', 'related_process']
        widgets = {
            'audit': forms.Select(attrs={'class': 'form-control'}),
            'finding_type': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'severity': forms.Select(attrs={'class': 'form-control'}),
            'related_process': forms.TextInput(attrs={'class': 'form-control'}),
        }