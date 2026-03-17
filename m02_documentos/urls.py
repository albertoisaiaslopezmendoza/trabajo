from django.urls import path
from . import views

app_name = 'm02_documentos'

urlpatterns = [
    path('', views.documento_list, name='lista'),
    path('nuevo/', views.documento_create, name='crear'),
    path('editar/<int:pk>/', views.documento_update, name='editar'),
    path('pdf/<int:pk>/', views.documento_pdf, name='pdf'),
]