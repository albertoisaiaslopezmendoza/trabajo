# i_m16_control_datos_audit_trail/urls.py
from django.urls import path
from . import views

app_name = 'i_m16_control_datos_audit_trail'

urlpatterns = [
    # Ruta principal del dashboard del módulo
    path('', views.dashboard, name='dashboard'),
]