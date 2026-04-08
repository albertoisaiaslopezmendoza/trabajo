from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_muestreo, name='c_m03_dashboard'),
    path('nueva/', views.nueva_muestra, name='c_m03_nueva_muestra'),
    path('custodia/<int:muestra_id>/', views.detalle_custodia, name='c_m03_custodia'),
]