from django import forms
from .models import AccionCorrectiva

class AccionCorrectivaForm(forms.ModelForm):
    class Meta:
        model = AccionCorrectiva
        fields = [
            'codigo_ac', 'origen', 'referencia_origen', 'fecha_apertura',
            'descripcion_no_conformidad', 'analisis_causa_raiz', 'estado',
            'acciones_implementadas', 'responsable_implementacion',
            'fecha_limite_implementacion', 'evaluacion_eficacia',
            'es_eficaz', 'requiere_actualizar_riesgos'
        ]
        widgets = {
            'codigo_ac': forms.TextInput(attrs={'class': 'form-control'}),
            'origen': forms.Select(attrs={'class': 'form-select'}),
            'referencia_origen': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Opcional'}),
            'fecha_apertura': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'descripcion_no_conformidad': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'analisis_causa_raiz': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'acciones_implementadas': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'responsable_implementacion': forms.Select(attrs={'class': 'form-select'}),
            'fecha_limite_implementacion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'evaluacion_eficacia': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'es_eficaz': forms.CheckboxInput(attrs={'class': 'form-check-input ms-2'}),
            'requiere_actualizar_riesgos': forms.CheckboxInput(attrs={'class': 'form-check-input ms-2'}),
        }