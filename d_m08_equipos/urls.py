from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_equipos, name='d_m08_dashboard'),
    path('nuevo/', views.nuevo_equipo, name='d_m08_nuevo'),
    path('equipo/<int:equipo_id>/', views.detalle_equipo, name='d_m08_detalle'),
]