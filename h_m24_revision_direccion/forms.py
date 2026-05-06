# h_m24_revision_direccion/forms.py
from django import forms
from .models import RevisionDireccion, AcuerdoRMD

class RevisionDireccionForm(forms.ModelForm):
    class Meta:
        model = RevisionDireccion
        fields = ['codigo_mr', 'fecha_revision', 'resumen', 'estatus']
        widgets = {
            'codigo_mr': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. RMD-2026-01'}),
            'fecha_revision': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'resumen': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'estatus': forms.Select(attrs={'class': 'form-control'}),
        }

class AcuerdoRMDForm(forms.ModelForm):
    class Meta:
        model = AcuerdoRMD
        fields = ['revision', 'accion', 'responsable', 'fecha_limite', 'estatus']
        widgets = {
            'revision': forms.Select(attrs={'class': 'form-control'}),
            'accion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'responsable': forms.Select(attrs={'class': 'form-control'}),
            'fecha_limite': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'estatus': forms.Select(attrs={'class': 'form-control'}),
        }