from django import forms
from .models import TrabajoNoConforme

class TrabajoNoConformeForm(forms.ModelForm):
    class Meta:
        model = TrabajoNoConforme
        fields = [
            'codigo_tnc', 'estado', 'descripcion_no_conformidad',
            'acciones_inmediatas', 'evaluacion_importancia', 'impacto',
            'responsable_evaluacion', 'decision_aceptabilidad',
            'requiere_notificar_cliente', 'cliente_notificado',
            'autoriza_reanudar', 'requiere_accion_correctiva'
        ]
        widgets = {
            'codigo_tnc': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
            'descripcion_no_conformidad': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'acciones_inmediatas': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'evaluacion_importancia': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'impacto': forms.Select(attrs={'class': 'form-control'}),
            'responsable_evaluacion': forms.Select(attrs={'class': 'form-control'}),
            'decision_aceptabilidad': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'requiere_notificar_cliente': forms.CheckboxInput(attrs={'class': 'form-check-input ms-2'}),
            'cliente_notificado': forms.CheckboxInput(attrs={'class': 'form-check-input ms-2'}),
            'autoriza_reanudar': forms.Select(attrs={'class': 'form-control'}),
            'requiere_accion_correctiva': forms.CheckboxInput(attrs={'class': 'form-check-input ms-2'}),
        }