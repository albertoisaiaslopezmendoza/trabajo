# b_m02_clientes/forms.py
from django import forms
from .models import Cliente, AcuerdoConfidencialidad

class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = ['nombre_empresa', 'rfc', 'contacto_principal', 'email', 'telefono', 'direccion', 'activo']
        widgets = {
            'nombre_empresa': forms.TextInput(attrs={'class': 'form-control'}),
            'rfc': forms.TextInput(attrs={'class': 'form-control'}),
            'contacto_principal': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'direccion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'activo': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class AcuerdoConfidencialidadForm(forms.ModelForm):
    class Meta:
        model = AcuerdoConfidencialidad
        fields = ['cliente', 'fecha_firma', 'fecha_expiracion', 'archivo_acuerdo', 'estado']
        widgets = {
            'cliente': forms.Select(attrs={'class': 'form-control'}),
            'fecha_firma': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_expiracion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'archivo_acuerdo': forms.FileInput(attrs={'class': 'form-control'}),
            'estado': forms.Select(attrs={'class': 'form-control'}),
        }