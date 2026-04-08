from django import forms
from .models import PerfilPuesto, PerfilEmpleado

class PerfilPuestoForm(forms.ModelForm):
    class Meta:
        model = PerfilPuesto
        fields = '__all__'
        widgets = {
            'responsabilidades': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'autoridades': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'competencias_requeridas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class PerfilEmpleadoForm(forms.ModelForm):
    # Añadimos el campo de escritura libre con soporte para autocompletar
    nombre_puesto = forms.CharField(
        max_length=100,
        required=True,
        label="Perfil de Puesto",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Escriba o seleccione el puesto del empleado',
            'list': 'lista-puestos' # Conecta con el datalist de tu HTML
        })
    )

    class Meta:
        model = PerfilEmpleado
        # Quitamos 'puesto' de aquí para manejarlo por nuestra cuenta con 'nombre_puesto'
        fields = ['usuario', 'es_suplente_de', 'fecha_ingreso', 'firma_digital']
        widgets = {
            'usuario': forms.Select(attrs={'class': 'form-select'}),
            'es_suplente_de': forms.Select(attrs={'class': 'form-select'}),
            'fecha_ingreso': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'firma_digital': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }