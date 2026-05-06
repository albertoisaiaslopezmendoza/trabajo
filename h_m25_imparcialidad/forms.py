# h_m25_imparcialidad/forms.py
from django import forms
from .models import DeclaracionImparcialidad, ConflictoInteres, Mitigacion

class DeclaracionForm(forms.ModelForm):
    class Meta:
        model = DeclaracionImparcialidad
        fields = ['usuario', 'acepta_politicas', 'notas']
        widgets = {
            'usuario': forms.Select(attrs={'class': 'form-control'}),
            'acepta_politicas': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'notas': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }

class ConflictoForm(forms.ModelForm):
    class Meta:
        model = ConflictoInteres
        fields = ['usuario_reporta', 'descripcion', 'nivel_riesgo', 'estatus']
        widgets = {
            'usuario_reporta': forms.Select(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'nivel_riesgo': forms.Select(attrs={'class': 'form-control'}),
            'estatus': forms.Select(attrs={'class': 'form-control'}),
        }

class MitigacionForm(forms.ModelForm):
    class Meta:
        model = Mitigacion
        fields = ['conflicto', 'descripcion_medida', 'fecha_implementacion', 'responsable']
        widgets = {
            'conflicto': forms.Select(attrs={'class': 'form-control'}),
            'descripcion_medida': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'fecha_implementacion': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'responsable': forms.Select(attrs={'class': 'form-control'}),
        }