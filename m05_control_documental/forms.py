from django import forms
from .models import DocumentoControlado


class DocumentoForm(forms.ModelForm):
    class Meta:
        model = DocumentoControlado
        fields = '__all__'
        # Solo definimos atributos específicos de HTML como el tamaño de las filas (rows)
        widgets = {
            'contenido': forms.Textarea(attrs={'rows': 4}),
            'cambios': forms.Textarea(attrs={'rows': 2}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Iteramos sobre todos los campos del formulario para agregar las clases estéticas
        for field_name, field in self.fields.items():
            # Si el campo es un selector (desplegable)
            if isinstance(field.widget, forms.Select):
                field.widget.attrs.update({
                    'class': 'form-select bg-dark text-white border-secondary'
                })
            # Si el campo es una casilla de verificación (checkbox)
            elif isinstance(field.widget, forms.CheckboxInput):
                field.widget.attrs.update({
                    'class': 'form-check-input bg-dark border-secondary'
                })
            # Para todos los demás campos (texto, números, fechas, etc.)
            else:
                field.widget.attrs.update({
                    'class': 'form-control bg-dark text-white border-secondary'
                })