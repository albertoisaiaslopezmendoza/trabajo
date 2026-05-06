# i_m16_control_datos_audit_trail/views.py
from django.shortcuts import render
from a00_auditoria.models import AuditLog


def dashboard(request):
    """
    Vista principal del módulo de Control de Datos y Audit Trail.
    Obtiene los registros de auditoría ordenados por los más recientes.
    """
    # Cambiamos '-ts' por '-created_at' según la estructura real de tu modelo
    logs = AuditLog.objects.all().order_by('-created_at')[:200]

    context = {
        'logs': logs,
        'titulo_modulo': 'M16 - Control de Datos y Audit Trail'
    }
    return render(request, 'i_m16_control_datos_audit_trail/dashboard.html', context)