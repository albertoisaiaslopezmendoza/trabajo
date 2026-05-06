from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='m22_dashboard'),
    path('nuevo/', views.crear_registro, name='m22_nuevo'),
    path('editar/<int:pk>/', views.editar_registro, name='m22_editar'),
]