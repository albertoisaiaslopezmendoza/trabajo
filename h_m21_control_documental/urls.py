from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='m21_dashboard'),
    path('nuevo/', views.crear_documento, name='m21_nuevo'),
    path('editar/<int:pk>/', views.editar_documento, name='m21_editar'),
    path('nueva-version/<int:pk>/', views.generar_nueva_version, name='m21_nueva_version'),
]