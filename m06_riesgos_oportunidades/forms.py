from django import forms
from .models import RiesgoOportunidad

class RiesgoOportunidadForm(forms.ModelForm):
    class Meta:
        model = RiesgoOportunidad
        fields = '__all__'
        widgets = {
            'fecha_objetivo': forms.DateInput(attrs={'type': 'date'}),
            'probabilidad': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'impacto': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'descripcion': forms.Textarea(attrs={'rows': 3}),
            'causa': forms.Textarea(attrs={'rows': 2}),
            'consecuencia': forms.Textarea(attrs={'rows': 2}),
            'control_actual': forms.Textarea(attrs={'rows': 2}),
            'accion_plan': forms.Textarea(attrs={'rows': 2}),
            'evidencia': forms.Textarea(attrs={'rows': 2}),
        }