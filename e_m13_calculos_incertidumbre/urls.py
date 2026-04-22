from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_calculos, name='e_m13_dashboard'),
    path('registrar/', views.registrar_calculo, name='e_m13_registrar'),
]