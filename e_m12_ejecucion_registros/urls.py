from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_registros, name='e_m12_dashboard'),
    path('crear/', views.crear_editar_registro, name='e_m12_crear'),
    path('editar/<int:registro_id>/', views.crear_editar_registro, name='e_m12_editar'),
]