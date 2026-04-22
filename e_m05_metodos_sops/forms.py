from django import forms
from .models import MetodoSOP

class MetodoSOPForm(forms.ModelForm):
    class Meta:
        model = MetodoSOP
        fields = ['codigo', 'titulo', 'tipo', 'version', 'fecha_emision', 'fecha_proxima_revision', 'estado', 'archivo_pdf']
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. LABCOR-MET-01'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'version': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_emision': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_proxima_revision': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'archivo_pdf': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }