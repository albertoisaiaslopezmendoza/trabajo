from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_competencia, name='e_m06_dashboard'),
    path('autorizar/', views.registrar_autorizacion, name='e_m06_autorizar'),
    path('certificado/<int:usuario_id>/', views.descargar_certificado_competencia, name='e_m06_certificado_pdf'),
]