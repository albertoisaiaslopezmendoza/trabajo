from django import forms
from .models import DeclaracionImparcialidad

class DeclaracionForm(forms.ModelForm):
    # Campo oculto para guardar la data de la firma (Base64 desde JS)
    firma_data_url = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = DeclaracionImparcialidad
        fields = ['nombre_completo', 'puesto', 'area',
                  'acepta_imparcialidad', 'acepta_confidentialidad', 'acepta_privacidad',
                  'observaciones']
        widgets = {
            'nombre_completo': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tu nombre completo'}),
            'puesto': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Analista de Laboratorio'}),
            'area': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Cromatografía'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

    def clean(self):
        cleaned_data = super().clean()

        # 1. Validar Checkboxes
        if not all([cleaned_data.get('acepta_imparcialidad'),
                    cleaned_data.get('acepta_confidentialidad'),
                    cleaned_data.get('acepta_privacidad')]):
            raise forms.ValidationError("Debe leer y aceptar las 3 declaraciones obligatorias.")

        # 2. Validar que se haya dibujado la firma
        firma_data = cleaned_data.get('firma_data_url')
        if not firma_data:
            raise forms.ValidationError("Debe firmar el documento en el recuadro digital.")

        return cleaned_data