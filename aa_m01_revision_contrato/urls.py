from django.urls import path
from . import views

app_name = 'aa_m01_revision_contrato'

urlpatterns = [
    path('', views.lista_contratos, name='lista'),
    path('nuevo/', views.crear_contrato, name='crear'),
    path('editar/<int:pk>/', views.editar_contrato, name='editar'),
]