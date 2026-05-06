# h_m24_revision_direccion/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_revision, name='m24_dashboard'),
]