# h_m25_imparcialidad/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_imparcialidad, name='m25_dashboard'),
]