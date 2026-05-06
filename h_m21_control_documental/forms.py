from django import forms
from .models import DocumentoSGC

class DocumentoSGCForm(forms.ModelForm):
    class Meta:
        model = DocumentoSGC
        fields = [
            'codigo', 'titulo', 'tipo', 'estado', 'descripcion_cambios',
            'enlace_archivo', 'revisado_por', 'aprobado_por',
            'fecha_aprobacion', 'fecha_proxima_revision'
        ]
        widgets = {
            'codigo': forms.TextInput(attrs={'class': 'form-control'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'descripcion_cambios': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Describa los cambios principales si es una versión > 1'}),
            'enlace_archivo': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://...'}),
            'revisado_por': forms.Select(attrs={'class': 'form-select'}),
            'aprobado_por': forms.Select(attrs={'class': 'form-select'}),
            'fecha_aprobacion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_proxima_revision': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }