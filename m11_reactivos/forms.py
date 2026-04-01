# m11_reactivos/forms.py
from django import forms
from .models import Reactivo, LoteReactivo, Proveedor

class ReactivoForm(forms.ModelForm):
    """
    Formulario para registrar un nuevo Reactivo en el catálogo.
    """
    class Meta:
        model = Reactivo
        fields = ['nombre', 'descripcion', 'proveedor', 'ficha_seguridad']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Ácido Clorhídrico'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'proveedor': forms.Select(attrs={'class': 'form-select'}),
            'ficha_seguridad': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class LoteReactivoForm(forms.ModelForm):
    """
    Formulario para registrar el ingreso de un nuevo Lote de un reactivo existente.
    """
    class Meta:
        model = LoteReactivo
        fields = ['reactivo', 'numero_lote', 'fecha_recepcion', 'fecha_caducidad', 'cantidad_recibida', 'unidad_medida', 'certificado_analisis']
        widgets = {
            'reactivo': forms.Select(attrs={'class': 'form-select'}),
            'numero_lote': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_recepcion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_caducidad': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'cantidad_recibida': forms.NumberInput(attrs={'class': 'form-control'}),
            'unidad_medida': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. ml, g, L'}),
            'certificado_analisis': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }