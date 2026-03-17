from django import forms
from .models import AccionCorrectiva

class AccionCorrectivaForm(forms.ModelForm):
    class Meta:
        model = AccionCorrectiva
        fields = '__all__'
        exclude = ['causa_raiz', 'fecha_cierre']  # Estos se autocalculan o actualizan al cerrar
        widgets = {
            'fecha_objetivo': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'firma': forms.HiddenInput(),  # Se llenará con JavaScript desde un Canvas
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Iteramos sobre los campos para darles clases específicas según su tipo
        for field_name, field in self.fields.items():
            if isinstance(field.widget, forms.CheckboxInput):
                # Clase especial de Bootstrap para checkboxes
                field.widget.attrs['class'] = 'form-check-input'
            elif isinstance(field.widget, forms.Select):
                # Clase especial de Bootstrap para selects (desplegables)
                field.widget.attrs['class'] = 'form-select'
            elif isinstance(field.widget, forms.Textarea):
                # A los cuadros de texto grandes les ponemos form-control y limitamos su altura
                field.widget.attrs['class'] = 'form-control'
                field.widget.attrs['rows'] = 3  # ¡Esto evitará que los cuadros se vean enormes!
            else:
                # A los campos normales de texto les aplicamos el estándar
                field.widget.attrs['class'] = 'form-control'