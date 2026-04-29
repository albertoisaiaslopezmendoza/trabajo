from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='m20_dashboard'),
    path('nueva/', views.crear_ac, name='m20_nueva'),
    path('editar/<int:pk>/', views.editar_ac, name='m20_editar'),
]