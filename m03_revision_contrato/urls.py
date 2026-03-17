from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_m03, name='m03_dashboard'),
    path('nueva/', views.crear_revision, name='m03_crear'),
    path('api/cotizacion/<int:cotizacion_id>/', views.api_cotizacion_info, name='m03_api_cot'),
]