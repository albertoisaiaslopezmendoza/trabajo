# m11_reactivos/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='m11_dashboard'),

    # Rutas para Reactivos
    path('reactivos/', views.lista_reactivos, name='m11_lista_reactivos'),
    path('reactivos/nuevo/', views.nuevo_reactivo, name='m11_nuevo_reactivo'),

    # Rutas para Lotes
    path('lotes/', views.lista_lotes, name='m11_lista_lotes'),
    path('lotes/nuevo/', views.nuevo_lote, name='m11_nuevo_lote'),
]