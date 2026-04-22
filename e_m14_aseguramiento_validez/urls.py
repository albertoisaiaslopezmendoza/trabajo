from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_qc, name='e_m14_dashboard'),
    path('registrar/', views.crear_editar_qc, name='e_m14_crear'),
    path('editar/<int:qc_id>/', views.crear_editar_qc, name='e_m14_editar'),
]