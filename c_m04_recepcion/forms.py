from django import forms
from .models import RecepcionMuestra

class RecepcionForm(forms.ModelForm):
    class Meta:
        model = RecepcionMuestra
        fields = ['conforme', 'observaciones_integridad', 'ubicacion_fisica', 'condiciones_almacenamiento', 'estado_actual']
        widgets = {
            'observaciones_integridad': forms.Textarea(attrs={'rows': 3}),
        }