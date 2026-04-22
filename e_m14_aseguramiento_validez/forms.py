from django import forms
from .models import RegistroQC

class RegistroQCForm(forms.ModelForm):
    class Meta:
        model = RegistroQC
        fields = ['folio_qc', 'metodo', 'registro_tecnico_asociado', 'tipo_control', 'fecha_ejecucion', 'criterios_aceptacion', 'resultados_obtenidos', 'es_conforme', 'evidencia_adjunta', 'estado']
        widgets = {
            'folio_qc': forms.TextInput(attrs={'class': 'form-control'}),
            'metodo': forms.Select(attrs={'class': 'form-select'}),
            'registro_tecnico_asociado': forms.Select(attrs={'class': 'form-select'}),
            'tipo_control': forms.Select(attrs={'class': 'form-select'}),
            'fecha_ejecucion': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'criterios_aceptacion': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'resultados_obtenidos': forms.Textarea(attrs={'class': 'form-control font-monospace', 'rows': 3}),
            'es_conforme': forms.CheckboxInput(attrs={'class': 'form-check-input ms-2'}),
            'evidencia_adjunta': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-select fw-bold'}),
        }