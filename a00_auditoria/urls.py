# a00_auditoria/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='a00_dashboard'),
    path('log-test/', views.log_test, name='a00_log_test'),
    path('init-schema/', views.init_schema, name='a00_init_schema'),
]