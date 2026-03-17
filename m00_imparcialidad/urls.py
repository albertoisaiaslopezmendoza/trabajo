from django.urls import path
from . import views

app_name = 'm00_imparcialidad'

urlpatterns = [
    # El nombre 'dashboard' conecta con {% url 'm00_imparcialidad:dashboard' %}
    path('', views.dashboard_m00, name='dashboard'),
    path('nuevo/', views.crear_declaracion, name='crear'),
    path('pdf/<int:decl_id>/', views.descargar_pdf, name='pdf'),
]