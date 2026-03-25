# a03_mapa_procesos/urls.py
from django.urls import path
from . import views

app_name = 'a03_mapa_procesos'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
]