from django.urls import path
from . import views

app_name = 'm04_manual'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('nueva-revision/', views.nueva_revision, name='nueva_revision'),
    path('aprobar/<int:pk>/', views.aprobar_manual, name='aprobar_manual'),
    path('distribucion/<int:pk>/', views.agregar_distribucion, name='agregar_distribucion'),
    path('exportar/<int:pk>/', views.exportar_pdf, name='exportar_pdf'),
]