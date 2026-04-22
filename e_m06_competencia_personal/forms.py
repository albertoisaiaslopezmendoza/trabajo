from django import forms
from .models import Capacitacion, AutorizacionMetodo

class CapacitacionForm(forms.ModelForm):
    class Meta:
        model = Capacitacion
        fields = ['titulo', 'empleado', 'tipo', 'fecha_inicio', 'fecha_fin', 'instructor', 'evidencia_pdf', 'estado']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'empleado': forms.Select(attrs={'class': 'form-select'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'instructor': forms.TextInput(attrs={'class': 'form-control'}),
            'evidencia_pdf': forms.FileInput(attrs={'class': 'form-control'}),
        }

class AutorizacionForm(forms.ModelForm):
    class Meta:
        model = AutorizacionMetodo
        fields = ['personal', 'metodo', 'fecha_autorizacion', 'observaciones']
        widgets = {
            'fecha_autorizacion': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'personal': forms.Select(attrs={'class': 'form-select'}),
            'metodo': forms.Select(attrs={'class': 'form-select'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }