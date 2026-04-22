from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_metodos, name='e_m05_dashboard'),
    path('crear/', views.crear_metodo, name='e_m05_crear'),
]