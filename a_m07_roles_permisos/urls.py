from django.urls import path
from . import views

app_name = 'a_m07_roles_permisos'

urlpatterns = [
    path('personal/', views.lista_personal, name='lista_personal'),
    path('personal/nuevo/', views.crear_personal, name='crear_personal'),
    path('puestos/', views.lista_puestos, name='lista_puestos'),
    path('puestos/nuevo/', views.crear_puesto, name='crear_puesto'),
]