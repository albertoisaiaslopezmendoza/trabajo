from django import forms
from .models import RegistroCalidad

class RegistroCalidadForm(forms.ModelForm):
    class Meta:
        model = RegistroCalidad
        fields = [
            'codigo_registro', 'titulo', 'tipo', 'medio_almacenamiento',
            'ubicacion_almacenamiento', 'metodo_proteccion', 'tiempo_retencion_anios',
            'metodo_disposicion', 'responsable_custodia', 'estado',
            'fecha_creacion_registro', 'observaciones'
        ]
        widgets = {
            'codigo_registro': forms.TextInput(attrs={'class': 'form-control'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-select'}),
            'medio_almacenamiento': forms.Select(attrs={'class': 'form-select'}),
            'ubicacion_almacenamiento': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Archivero 3 / Servidor SharePoint'}),
            'metodo_proteccion': forms.TextInput(attrs={'class': 'form-control'}),
            'tiempo_retencion_anios': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'metodo_disposicion': forms.Select(attrs={'class': 'form-select'}),
            'responsable_custodia': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'fecha_creacion_registro': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Si cambia el estado a Destruido, indique aquí los detalles (Ej. Acta de trituración)'}),
        }