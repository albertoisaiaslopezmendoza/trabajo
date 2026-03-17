from django.urls import path
from . import views

# Definimos el nombre de la aplicación para poder referenciar las urls fácilmente
app_name = 'm05_control_documental'

# Esta es la lista "iterable" que Django estaba buscando y no encontraba
urlpatterns = [
    # Ruta para el dashboard principal (ej. /m05/)
    path('', views.dashboard, name='dashboard'),
    # Ruta para crear el documento (ej. /m05/nuevo/)
    path('nuevo/', views.crear_documento, name='crear_documento'),
]