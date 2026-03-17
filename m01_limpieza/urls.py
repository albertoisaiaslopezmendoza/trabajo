from django.urls import path
from . import views

urlpatterns = [
    path('', views.m01_dashboard, name='m01_dashboard'),
]