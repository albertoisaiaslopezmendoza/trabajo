from django import forms
from .models import Muestra, CadenaCustodia

class MuestraForm(forms.ModelForm):
    class Meta:
        model = Muestra
        fields = ['codigo', 'descripcion', 'metodo_muestreo', 'fecha_muestreo', 'condiciones_ambientales', 'responsable_muestreo']
        widgets = {
            'fecha_muestreo': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'rows': 3}),
        }

class CadenaCustodiaForm(forms.ModelForm):
    class Meta:
        model = CadenaCustodia
        fields = ['entregado_por', 'recibido_por', 'comentarios']
        widgets = {
            'comentarios': forms.Textarea(attrs={'rows': 2}),
        }