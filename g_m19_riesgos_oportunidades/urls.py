from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='m19_dashboard'),
    path('nuevo/', views.crear_ro, name='m19_nuevo'),
    path('editar/<int:pk>/', views.editar_ro, name='m19_editar'),
]