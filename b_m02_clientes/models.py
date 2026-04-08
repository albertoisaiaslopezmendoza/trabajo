from django.db import models
from django.contrib.auth.models import User


class Cliente(models.Model):
    nombre_empresa = models.CharField(max_length=200, verbose_name="Nombre de la Empresa o Razón Social")
    rfc = models.CharField(max_length=20, blank=True, null=True, verbose_name="RFC")
    contacto_principal = models.CharField(max_length=150, verbose_name="Nombre del Contacto")
    email = models.EmailField(verbose_name="Correo Electrónico")
    telefono = models.CharField(max_length=20, verbose_name="Teléfono")
    direccion = models.TextField(blank=True, null=True, verbose_name="Dirección Fiscal")
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True, verbose_name="¿Es un cliente activo?")

    def __str__(self):
        return f"{self.nombre_empresa} - {self.contacto_principal}"


class AcuerdoConfidencialidad(models.Model):
    ESTADOS = [
        ('VIGENTE', 'Vigente'),
        ('EXPIRADO', 'Expirado'),
        ('CANCELADO', 'Cancelado'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="acuerdos")
    fecha_firma = models.DateField(verbose_name="Fecha de Firma del Acuerdo")
    fecha_expiracion = models.DateField(blank=True, null=True, verbose_name="Fecha de Expiración")
    # AQUÍ ESTÁ LA CORRECCIÓN: cambiamos upload_path por upload_to
    archivo_acuerdo = models.FileField(upload_to='acuerdos_confidencialidad/', verbose_name="Archivo (PDF)")
    estado = models.CharField(max_length=20, choices=ESTADOS, default='VIGENTE')
    registrado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Acuerdo: {self.cliente.nombre_empresa} ({self.estado})"