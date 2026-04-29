from django import forms
from .models import InformeCertificado

class InformeCertificadoForm(forms.ModelForm):
    class Meta:
        model = InformeCertificado
        fields = [
            'codigo_informe', 'tipo', 'estado',
            'declaracion_conformidad', 'opiniones_interpretaciones'
        ]
        widgets = {
            'codigo_informe': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'declaracion_conformidad': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'opiniones_interpretaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }