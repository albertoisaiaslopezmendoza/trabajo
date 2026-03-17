from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Esto usa la vista de login estándar de Django
    path('', auth_views.LoginView.as_view(template_name='login/login.html'), name='login'),
    # Ruta para cerrar sesión (opcional pero recomendada)
    path('logout/', views.signout, name='logout'),
]