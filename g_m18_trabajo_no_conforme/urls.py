from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='m18_dashboard'),
    path('nuevo/', views.crear_tnc, name='m18_nuevo'),
    path('editar/<int:pk>/', views.editar_tnc, name='m18_editar'),
]