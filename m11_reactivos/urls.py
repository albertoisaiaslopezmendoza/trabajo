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

    # NUEVO: Rutas para Proveedores (ISO 17025: 6.6)
    path('proveedores/', views.lista_proveedores, name='m11_lista_proveedores'),
    path('proveedores/nuevo/', views.nuevo_proveedor, name='m11_nuevo_proveedor'),

    # NUEVO: Rutas para Servicios Externos (ISO 17025: 6.6)
    path('servicios/', views.lista_servicios, name='m11_lista_servicios'),
    path('servicios/nuevo/', views.nuevo_servicio, name='m11_nuevo_servicio'),
]