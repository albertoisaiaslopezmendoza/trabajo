from django import forms
from .models import PerfilPuesto, PerfilEmpleado

class PerfilPuestoForm(forms.ModelForm):
    class Meta:
        model = PerfilPuesto
        fields = '__all__'
        widgets = {
            'responsabilidades': forms.Textarea(attrs={'rows': 3}),
            'autoridades': forms.Textarea(attrs={'rows': 3}),
            'competencias_requeridas': forms.Textarea(attrs={'rows': 3}),
        }

class PerfilEmpleadoForm(forms.ModelForm):
    class Meta:
        model = PerfilEmpleado
        fields = ['usuario', 'puesto', 'es_suplente_de', 'fecha_ingreso', 'firma_digital']
        widgets = {
            'fecha_ingreso': forms.DateInput(attrs={'type': 'date'}),
        }