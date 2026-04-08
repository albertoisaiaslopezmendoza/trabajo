# b_m02_clientes/urls.py
from django.urls import path
from . import views

app_name = 'b_m02_clientes'

urlpatterns = [
    path('', views.dashboard_clientes, name='dashboard'),
    path('nuevo-cliente/', views.registrar_cliente, name='nuevo_cliente'),
    path('nuevo-acuerdo/', views.registrar_acuerdo, name='nuevo_acuerdo'),
]