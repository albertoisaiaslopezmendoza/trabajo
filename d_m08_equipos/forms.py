from django import forms
from .models import Equipo, Mantenimiento, Calibracion

class EquipoForm(forms.ModelForm):
    class Meta:
        model = Equipo
        fields = ['codigo_interno', 'nombre', 'marca', 'modelo', 'serie', 'ubicacion', 'fecha_ingreso', 'estado']
        widgets = {'fecha_ingreso': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})}

class MantenimientoForm(forms.ModelForm):
    class Meta:
        model = Mantenimiento
        fields = ['fecha_servicio', 'tipo', 'descripcion', 'proximo_mantenimiento', 'realizado_por']
        widgets = {
            'fecha_servicio': forms.DateInput(attrs={'type': 'date'}),
            'proximo_mantenimiento': forms.DateInput(attrs={'type': 'date'}),
        }