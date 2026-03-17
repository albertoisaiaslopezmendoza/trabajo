from django.urls import path
from . import views

# Declaramos el espacio de nombres (namespace) para esta aplicación
app_name = 'm06_riesgos_oportunidades'

urlpatterns = [
    path('', views.dashboard_m06, name='m06_dashboard'),
    path('exportar-excel/', views.exportar_excel_m06, name='m06_exportar_excel'),
]