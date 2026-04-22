from django import forms
from .models import RegistroTecnico

class RegistroTecnicoForm(forms.ModelForm):
    class Meta:
        model = RegistroTecnico
        fields = ['folio_registro', 'identificador_muestra', 'metodo', 'fecha_inicio', 'fecha_fin', 'datos_crudos', 'calculos_resultados', 'evidencia_adjunta', 'estado']
        widgets = {
            'folio_registro': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'RT-Año-Folio'}),
            'identificador_muestra': forms.TextInput(attrs={'class': 'form-control'}),
            'metodo': forms.Select(attrs={'class': 'form-select'}),
            'fecha_inicio': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'fecha_fin': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'datos_crudos': forms.Textarea(attrs={'class': 'form-control font-monospace bg-light', 'rows': 4}),
            'calculos_resultados': forms.Textarea(attrs={'class': 'form-control font-monospace bg-light', 'rows': 4}),
            'evidencia_adjunta': forms.FileInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-select fw-bold'}),
        }