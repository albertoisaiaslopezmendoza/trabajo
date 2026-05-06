# h_m24_revision_direccion/models.py
from django.db import models
from django.contrib.auth.models import User


class KPI(models.Model):
    """Modelo para registrar los Indicadores Clave de Desempeño."""
    nombre = models.CharField("Nombre del KPI", max_length=150)
    descripcion = models.TextField("Descripción", blank=True)
    meta = models.DecimalField("Meta Esperada", max_digits=10, decimal_places=2)
    valor_actual = models.DecimalField("Valor Actual", max_digits=10, decimal_places=2)
    ultima_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nombre} (Actual: {self.valor_actual} / Meta: {self.meta})"


class RevisionDireccion(models.Model):
    """Modelo para registrar las reuniones de revisión por la dirección."""
    STATUS_CHOICES = [
        ('OPEN', 'Abierta'),
        ('CLOSED', 'Cerrada'),
    ]

    codigo_mr = models.CharField("Código de Revisión", max_length=50, unique=True)
    fecha_revision = models.DateField("Fecha de Revisión")
    resumen = models.TextField("Resumen Ejecutivo")
    estatus = models.CharField("Estatus", max_length=15, choices=STATUS_CHOICES, default='OPEN')

    # minutes_attachment = models.FileField(upload_to='revisiones/', null=True, blank=True)

    def __str__(self):
        return f"{self.codigo_mr} - {self.fecha_revision}"


class AcuerdoRMD(models.Model):
    """Modelo para registrar las acciones y recursos asignados derivados de la revisión."""
    STATUS_CHOICES = [
        ('PENDING', 'Pendiente'),
        ('DONE', 'Realizado'),
        ('CLOSED', 'Cerrado'),
    ]

    revision = models.ForeignKey(RevisionDireccion, on_delete=models.CASCADE, related_name='acuerdos')
    accion = models.TextField("Acción / Recurso Asignado")
    responsable = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    fecha_limite = models.DateField("Fecha Límite")
    estatus = models.CharField("Estatus", max_length=15, choices=STATUS_CHOICES, default='PENDING')

    def __str__(self):
        return f"Acuerdo de {self.revision.codigo_mr} - Resp: {self.responsable}"