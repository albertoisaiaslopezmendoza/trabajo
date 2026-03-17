from django import forms
from .models import RevisionContrato


class RevisionForm(forms.ModelForm):
    class Meta:
        model = RevisionContrato
        fields = [
            'cotizacion', 'estado',
            'alcance_confirmado', 'capacidad_laboratorio', 'recursos_disponibles',
            'metodo_validado', 'incertidumbre_conocida', 'plazo_aceptado',
            'revision_previa_ok', 'cambios_detectados', 'descripcion_cambios',
            'observaciones'
        ]
        widgets = {
            'cotizacion': forms.Select(attrs={'class': 'form-select bg-dark text-white border-secondary'}),
            'estado': forms.Select(attrs={'class': 'form-select bg-dark text-white border-secondary'}),
            'descripcion_cambios': forms.Textarea(
                attrs={'class': 'form-control bg-dark text-white border-secondary', 'rows': 2}),
            'observaciones': forms.Textarea(
                attrs={'class': 'form-control bg-dark text-white border-secondary', 'rows': 2}),
        }

    def clean(self):
        cleaned_data = super().clean()
        estado = cleaned_data.get("estado")
        cambios = cleaned_data.get("cambios_detectados")
        desc_cambios = cleaned_data.get("descripcion_cambios")

        # Validación del Checklist para aprobar (Lógica original)
        checklist_keys = [
            'alcance_confirmado', 'capacidad_laboratorio', 'recursos_disponibles',
            'metodo_validado', 'incertidumbre_conocida', 'plazo_aceptado',
            'revision_previa_ok'
        ]

        if estado == 'APROBADO':
            for key in checklist_keys:
                if not cleaned_data.get(key):
                    raise forms.ValidationError(f"El campo '{self.fields[key].label}' es obligatorio para APROBAR.")

        if cambios and not desc_cambios:
            self.add_error('descripcion_cambios',
                           "Debe describir los cambios si marcó la casilla de cambios detectados.")

        return cleaned_data