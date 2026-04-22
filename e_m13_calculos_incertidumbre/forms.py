from django import forms
from .models import CalculoIncertidumbre, PresupuestoIncertidumbre

class CalculoIncertidumbreForm(forms.ModelForm):
    class Meta:
        model = CalculoIncertidumbre
        fields = ['registro_tecnico', 'presupuesto_utilizado', 'resultado_medicion', 'incertidumbre_combinada', 'unidades']
        widgets = {
            'registro_tecnico': forms.Select(attrs={'class': 'form-select'}),
            'presupuesto_utilizado': forms.Select(attrs={'class': 'form-select'}),
            'resultado_medicion': forms.NumberInput(attrs={'class': 'form-control font-monospace', 'step': 'any'}),
            'incertidumbre_combinada': forms.NumberInput(attrs={'class': 'form-control font-monospace', 'step': 'any'}),
            'unidades': forms.TextInput(attrs={'class': 'form-control'}),
        }
        help_texts = {
            'incertidumbre_combinada': 'Ingrese la incertidumbre combinada (uc). El sistema multiplicará por k automáticamente.'
        }