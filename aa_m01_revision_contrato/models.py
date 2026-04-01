from django.db import models
from django.contrib.auth.models import User


class RevisionContrato(models.Model):
    ESTADO_CHOICES = [
        ('PENDIENTE', 'Pendiente de Revisión'),
        ('APROBADO', 'Aprobado'),
        ('RECHAZADO', 'Rechazado'),
    ]

    folio = models.CharField(max_length=50, unique=True, verbose_name="Folio de Solicitud")
    cliente = models.CharField(max_length=150, verbose_name="Cliente")
    descripcion_solicitud = models.TextField(verbose_name="Descripción de la Solicitud")
    metodo_ensayo = models.CharField(max_length=100, verbose_name="Método Solicitado")

    # Verificaciones obligatorias ISO 17025 (Cláusula 7.1)
    capacidad_recursos = models.BooleanField(default=False, verbose_name="¿Tenemos capacidad y recursos?")
    metodo_apropiado = models.BooleanField(default=False, verbose_name="¿El método es apropiado y vigente?")

    estado = models.CharField(max_length=15, choices=ESTADO_CHOICES, default='PENDIENTE', verbose_name="Estado")
    comentarios = models.TextField(blank=True, null=True, verbose_name="Comentarios / Desviaciones")

    fecha_solicitud = models.DateField(auto_now_add=True)
    revisado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                     verbose_name="Revisado por")
    fecha_revision = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Revisión de Contrato"
        verbose_name_plural = "Revisiones de Contratos"

    def __str__(self):
        return f"{self.folio} - {self.cliente}"