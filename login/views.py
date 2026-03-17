from django.shortcuts import render, redirect
from django.contrib.auth import logout # Importar logout

# ... (tú código existente) ...

def signout(request):
    """Cierra la sesión del usuario y redirige al login"""
    logout(request)
    return redirect('login') # Asegúrate que 'login' es el nombre de tu url de inicio de sesión