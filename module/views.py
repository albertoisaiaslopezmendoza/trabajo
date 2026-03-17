from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# solo usuarios registrados
def inicio(request):
    context = {
        "app_title": "AuditReady Labs"
    }
    return render(request, 'inicio.html', context)