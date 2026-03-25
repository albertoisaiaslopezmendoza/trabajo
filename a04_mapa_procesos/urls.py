from django.urls import path
from . import views

app_name = 'a04_mapa_procesos'

urlpatterns = [
    # Esta ruta cargará la vista principal del mapa
    path('', views.mapa_view, name='mapa_procesos'),
]