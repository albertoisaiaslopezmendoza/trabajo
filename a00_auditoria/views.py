# a00_auditoria/views.py
import socket
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import AuditLog


def _best_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        try:
            return socket.gethostbyname(socket.gethostname())
        except Exception:
            return "Desconocida"


def _best_hostname():
    try:
        return socket.gethostname()
    except Exception:
        return "Desconocido"


@login_required
def dashboard(request):
    # Traemos los últimos 100 registros como en tu script original
    logs = AuditLog.objects.all()[:100]

    context = {
        'dsn': 'Conectado a través del ORM de Django (SQLite actual)',
        'hostname': _best_hostname(),
        'ip': _best_ip(),
        'logs': logs,
        'state': 'Listo para registrar eventos y visualizar auditoría.',
    }

    # Registrar la apertura del módulo silenciosamente
    AuditLog.objects.create(
        user_id=request.user.id,
        username=request.user.username,
        module="I00",
        action="OPEN_MODULE",
        details=f"Apertura del módulo de auditoría por {request.user.username}",
        ip_address=_best_ip(),
        hostname=_best_hostname(),
        app_name="LIMBS Web",
        level="INFO",
        ok=True,
    )

    return render(request, 'a00_auditoria/dashboard.html', context)


@login_required
def log_test(request):
    # Esta vista simula el botón "Registrar prueba"
    AuditLog.objects.create(
        user_id=request.user.id,
        username=request.user.username,
        module="I00",
        action="TEST_EVENT",
        details=f"Evento de prueba generado manualmente por {request.user.username}",
        ip_address=_best_ip(),
        hostname=_best_hostname(),
        app_name="LIMBS Web",
        level="INFO",
        ok=True,
        meta={"source": "manual_test"}
    )
    messages.success(request, "Evento de prueba registrado correctamente.")
    return redirect('a00_dashboard')


@login_required
def init_schema(request):
    # En Django, la BD se inicializa con makemigrations/migrate. 
    # Solo mostraremos un mensaje de éxito.
    messages.info(request,
                  "El esquema de base de datos es manejado por Django ORM de forma automática. Tabla 'audit_log' verificada.")
    return redirect('a00_dashboard')