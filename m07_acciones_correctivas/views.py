from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from .models import AccionCorrectiva
from .forms import AccionCorrectivaForm

class DashboardM07View(ListView):
    model = AccionCorrectiva
    template_name = 'm07_acciones_correctivas/dashboard.html'
    context_object_name = 'registros'
    ordering = ['-fecha_registro']

class CrearNCView(CreateView):
    model = AccionCorrectiva
    form_class = AccionCorrectivaForm
    template_name = 'm07_acciones_correctivas/form.html'
    success_url = reverse_lazy('m07_dashboard')

class EditarNCView(UpdateView):
    model = AccionCorrectiva
    form_class = AccionCorrectivaForm
    template_name = 'm07_acciones_correctivas/form.html'
    success_url = reverse_lazy('m07_dashboard')
    