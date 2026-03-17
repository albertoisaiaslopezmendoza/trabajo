from django import forms
from .models import ManualSGC, ManualDistribution

class ManualSGCForm(forms.ModelForm):
    class Meta:
        model = ManualSGC
        fields = ['doc_code', 'doc_title', 'version', 'fecha_vigencia', 'cambio_resumen', 'contenido']
        widgets = {
            'fecha_vigencia': forms.DateInput(attrs={'type': 'date', 'class': 'form-control bg-dark text-white border-secondary'}),
            'doc_code': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
            'doc_title': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
            'version': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
            # CORRECCIÓN: Textarea para resumen de cambios
            'cambio_resumen': forms.Textarea(attrs={'class': 'form-control bg-dark text-white border-secondary', 'rows': 2}),
            'contenido': forms.Textarea(attrs={'class': 'form-control bg-dark text-white border-secondary', 'rows': 15}),
        }

class DistributionForm(forms.ModelForm):
    class Meta:
        model = ManualDistribution
        fields = ['recipient_name', 'area', 'copy_type', 'delivery_method', 'delivered_on', 'ack_received', 'ack_on']
        widgets = {
            'recipient_name': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
            'area': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
            'copy_type': forms.Select(attrs={'class': 'form-select bg-dark text-white border-secondary'}),
            'delivery_method': forms.TextInput(attrs={'class': 'form-control bg-dark text-white border-secondary'}),
            'delivered_on': forms.DateInput(attrs={'type': 'date', 'class': 'form-control bg-dark text-white border-secondary'}),
            'ack_received': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'ack_on': forms.DateInput(attrs={'type': 'date', 'class': 'form-control bg-dark text-white border-secondary'}),
        }