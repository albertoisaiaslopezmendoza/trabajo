from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_recepcion, name='c_m04_dashboard'),
    path('entrada/<int:muestra_id>/', views.registrar_entrada, name='c_m04_registrar_entrada'),
]