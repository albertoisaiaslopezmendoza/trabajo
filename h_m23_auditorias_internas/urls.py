# h_m23_auditorias_internas/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_auditorias, name='m23_dashboard'),
]