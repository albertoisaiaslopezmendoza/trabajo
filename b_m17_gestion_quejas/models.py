# b_m17_gestion_quejas/models.py
from django.db import models
from django.contrib.auth.models import User


class Queja(models.Model):
    ESTADOS = [
        ('RECIBIDA', 'Recibida'),
        ('EN_INVESTIGACION', 'En Investigación'),
        ('RESUELTA', 'Resuelta'),
        ('CERRADA', 'Cerrada'),
    ]
    folio = models.CharField(max_length=50, unique=True, verbose_name="Folio de la Queja (Ej. Q-2026-001)")
    cliente = models.CharField(max_length=200, verbose_name="Cliente o Empresa que reporta")
    fecha_recepcion = models.DateField(verbose_name="Fecha de Recepción")
    descripcion = models.TextField(verbose_name="Descripción detallada de la queja")
    recibida_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Recibida por")
    estado = models.CharField(max_length=20, choices=ESTADOS, default='RECIBIDA')
    acuse_recibo_enviado = models.BooleanField(default=False,
                                               verbose_name="¿Se envió acuse de recibo al cliente? (Cláusula 7.9.3)")
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.folio} - {self.cliente} ({self.estado})"


class InvestigacionQueja(models.Model):
    queja = models.OneToOneField(Queja, on_delete=models.CASCADE, related_name='investigacion')
    responsable = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                    verbose_name="Responsable de la Investigación (Cláusula 7.9.5)")
    analisis_causas = models.TextField(verbose_name="Análisis de Causas")
    acciones_tomadas = models.TextField(verbose_name="Acciones Tomadas / Resolución")
    fecha_resolucion = models.DateField(verbose_name="Fecha de Resolución")
    notificacion_enviada = models.BooleanField(default=False,
                                               verbose_name="¿Se notificó formalmente el cierre al cliente? (Cláusula 7.9.6)")

    def __str__(self):
        return f"Investigación de {self.queja.folio}"