# b_m17_gestion_quejas/forms.py
from django import forms
from .models import Queja, InvestigacionQueja

class QuejaForm(forms.ModelForm):
    class Meta:
        model = Queja
        fields = ['folio', 'cliente', 'fecha_recepcion', 'descripcion', 'acuse_recibo_enviado']
        widgets = {
            'folio': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Q-AÑO-XXX'}),
            'cliente': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_recepcion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'acuse_recibo_enviado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class InvestigacionForm(forms.ModelForm):
    class Meta:
        model = InvestigacionQueja
        fields = ['analisis_causas', 'acciones_tomadas', 'fecha_resolucion', 'notificacion_enviada']
        widgets = {
            'analisis_causas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'acciones_tomadas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'fecha_resolucion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'notificacion_enviada': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }