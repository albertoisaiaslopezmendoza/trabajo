from django import forms
from .models import MaterialReferencia, UsoMaterial

class MaterialReferenciaForm(forms.ModelForm):
    class Meta:
        model = MaterialReferencia
        exclude = ['usuario_creacion', 'fecha_creacion', 'activo']
        widgets = {
            'fecha_recepcion': forms.DateInput(attrs={'type': 'date'}),
            'fecha_apertura': forms.DateInput(attrs={'type': 'date'}),
            'fecha_caducidad': forms.DateInput(attrs={'type': 'date'}),
        }

class UsoMaterialForm(forms.ModelForm):
    class Meta:
        model = UsoMaterial
        fields = ['motivo_uso', 'cantidad_utilizada', 'observaciones']
        widgets = {
            'observaciones': forms.Textarea(attrs={'rows': 2}),
        }