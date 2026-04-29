from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='m15_dashboard'),
    path('nuevo/', views.crear_informe, name='m15_nuevo'),
    path('editar/<int:pk>/', views.editar_informe, name='m15_editar'),
    path('enmienda/<int:pk>/', views.generar_enmienda, name='m15_enmienda'),
    path('descargar-pdf/<int:pk>/', views.descargar_pdf, name='m15_descargar_pdf'),
]