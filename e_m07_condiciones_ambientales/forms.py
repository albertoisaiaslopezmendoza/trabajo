from django import forms
from .models import RegistroAmbiental

class RegistroAmbientalForm(forms.ModelForm):
    class Meta:
        model = RegistroAmbiental
        fields = ['area', 'fecha_hora', 'temperatura', 'humedad', 'observaciones']
        widgets = {
            'area': forms.Select(attrs={'class': 'form-select'}),
            'fecha_hora': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'temperatura': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'humedad': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
        }