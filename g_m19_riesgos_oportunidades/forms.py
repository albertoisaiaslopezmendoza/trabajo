from django import forms
from .models import RiesgoOportunidad

class RiesgoOportunidadForm(forms.ModelForm):
    class Meta:
        model = RiesgoOportunidad
        fields = [
            'codigo_ro', 'tipo', 'origen', 'fecha_identificacion', 'descripcion',
            'probabilidad', 'impacto', 'estado', 'acciones_planificadas',
            'responsable_accion', 'fecha_limite', 'evaluacion_eficacia', 'eficaz'
        ]
        widgets = {
            'codigo_ro': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'origen': forms.Select(attrs={'class': 'form-select'}),
            'fecha_identificacion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'probabilidad': forms.Select(attrs={'class': 'form-select'}),
            'impacto': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'acciones_planificadas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'responsable_accion': forms.Select(attrs={'class': 'form-select'}),
            'fecha_limite': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'evaluacion_eficacia': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'eficaz': forms.CheckboxInput(attrs={'class': 'form-check-input ms-2'}),
        }