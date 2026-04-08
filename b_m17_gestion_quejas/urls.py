# b_m17_gestion_quejas/urls.py
from django.urls import path
from . import views

app_name = 'b_m17_gestion_quejas'

urlpatterns = [
    path('', views.dashboard_quejas, name='dashboard'),
    path('nueva/', views.registrar_queja, name='registrar_queja'),
    path('investigar/<int:queja_id>/', views.investigar_queja, name='investigar_queja'),
]