from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_condiciones, name='e_m07_dashboard'),
    path('registrar/', views.crear_registro_ambiental, name='e_m07_registrar'),
]