from django import forms
from django.forms import inlineformset_factory
from .models import Documento, CambioDocumento, DistribucionDocumento


class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        exclude = ['sistema']
        widgets = {
            # --- Inputs de Texto y Números ---
            'codigo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: M02-P01'}),
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'version': forms.NumberInput(attrs={'class': 'form-control'}),
            'vigencia_meses': forms.NumberInput(attrs={'class': 'form-control'}),

            # SOLUCIÓN: Cambiamos 'area' de forms.Select a forms.TextInput para texto libre
            'area': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: Laboratorio, Dirección...'}),

            # --- Selectores / Dropdowns ---
            'tipo_documento': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'elaboro': forms.Select(attrs={'class': 'form-select'}),
            'reviso': forms.Select(attrs={'class': 'form-select'}),
            'aprobo': forms.Select(attrs={'class': 'form-select'}),

            # --- Fechas ---
            'fecha_emision': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_firma_elaboro': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_firma_reviso': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'fecha_firma_aprobo': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),

            # --- Áreas de Texto ---
            'objetivo': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'alcance': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'responsabilidades': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'definiciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'procedimiento': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'registros': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'referencias': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'anexos': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'nota_control': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }


CambioFormSet = inlineformset_factory(
    Documento, CambioDocumento,
    fields=['revision', 'fecha', 'descripcion', 'elaboro', 'aprobo'],
    extra=1,
    can_delete=True,
    widgets={
        'revision': forms.NumberInput(attrs={'class': 'form-control form-control-sm'}),
        'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control form-control-sm'}),
        'descripcion': forms.Textarea(attrs={'rows': 1, 'class': 'form-control form-control-sm'}),
        # Nota: Aquí asumo que elaboro y aprobo son texto libre según tu modelo CambioDocumento
        'elaboro': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
        'aprobo': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
    }
)

DistribucionFormSet = inlineformset_factory(
    Documento, DistribucionDocumento,
    fields=['area', 'puesto', 'nombre', 'copia_controlada'],
    extra=1,
    can_delete=True,
    widgets={
        # SOLUCIÓN: Cambiamos 'area' en la tabla de distribución a TextInput
        'area': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
        'puesto': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
        'nombre': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
        'copia_controlada': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    }
)