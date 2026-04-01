from django import forms
from .models import RevisionContrato

class RevisionContratoForm(forms.ModelForm):
    class Meta:
        model = RevisionContrato
        fields = [
            'folio', 'cliente', 'descripcion_solicitud', 'metodo_ensayo',
            'capacidad_recursos', 'metodo_apropiado', 'estado', 'comentarios'
        ]
        widgets = {
            'descripcion_solicitud': forms.Textarea(attrs={'rows': 3}),
            'comentarios': forms.Textarea(attrs={'rows': 2}),
        }