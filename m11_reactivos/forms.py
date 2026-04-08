from django import forms
from .models import Reactivo, LoteReactivo, Proveedor, ServicioExterno

class ReactivoForm(forms.ModelForm):
    # Campo extra para permitir escritura libre del proveedor
    nombre_proveedor = forms.CharField(
        max_length=200,
        required=False,
        label="Proveedor",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Escriba o seleccione un proveedor',
            'list': 'lista-proveedores' # Conecta con un datalist en el HTML
        })
    )

    class Meta:
        model = Reactivo
        # Quitamos 'proveedor' de los campos directos para manejarlo manualmente a través de 'nombre_proveedor'
        fields = ['nombre', 'descripcion', 'ficha_seguridad']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Ácido Clorhídrico'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'ficha_seguridad': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class LoteReactivoForm(forms.ModelForm):
    class Meta:
        model = LoteReactivo
        fields = ['reactivo', 'numero_lote', 'fecha_recepcion', 'fecha_caducidad', 'cantidad_recibida', 'unidad_medida', 'certificado_analisis']
        widgets = {
            # Esto ya cumple con tu petición: enlaza automáticamente con los Reactivos registrados
            'reactivo': forms.Select(attrs={'class': 'form-select'}),
            'numero_lote': forms.TextInput(attrs={'class': 'form-control'}),
            'fecha_recepcion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'fecha_caducidad': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'cantidad_recibida': forms.NumberInput(attrs={'class': 'form-control'}),
            'unidad_medida': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. ml, g, L'}),
            'certificado_analisis': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = ['nombre', 'contacto', 'telefono', 'email', 'aprobado', 'fecha_evaluacion', 'comentarios']
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'contacto': forms.TextInput(attrs={'class': 'form-control'}),
            'telefono': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'aprobado': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'fecha_evaluacion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'comentarios': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

class ServicioExternoForm(forms.ModelForm):
    class Meta:
        model = ServicioExterno
        fields = ['descripcion', 'proveedor', 'fecha_servicio', 'certificado_servicio', 'conforme']
        widgets = {
            'descripcion': forms.TextInput(attrs={'class': 'form-control'}),
            'proveedor': forms.Select(attrs={'class': 'form-select'}),
            'fecha_servicio': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'certificado_servicio': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'conforme': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }