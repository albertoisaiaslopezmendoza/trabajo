from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_trazabilidad, name='d_m09_dashboard'),
    path('nuevo/', views.nuevo_mrc, name='d_m09_nuevo'),
    path('detalle/<int:mrc_id>/', views.detalle_mrc, name='d_m09_detalle'),
]