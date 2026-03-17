from django.urls import path
from . import views

urlpatterns = [
    path('', views.DashboardM07View.as_view(), name='m07_dashboard'),
    path('nuevo/', views.CrearNCView.as_view(), name='m07_nuevo'),
    path('editar/<int:pk>/', views.EditarNCView.as_view(), name='m07_editar'),
]