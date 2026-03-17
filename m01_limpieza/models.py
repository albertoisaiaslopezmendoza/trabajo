from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid


class ActivoLimpieza(models.Model):
    codigo_barras = models.CharField(max_length=100, unique=True)
    nombre = models.CharField(max_length=200, help_text="Nombre del activo o área")
    area = models.CharField(max_length=100, help_text="Zona física (ej. Laboratorio A)")
    frecuencia_dias = models.IntegerField(default=7, help_text="Cada cuántos días se debe limpiar")

    # CAMBIO: TextField en lugar de JSONField para facilitar el uso
    checklist_default = models.TextField(default="", blank=True,
                                         help_text="Escribe las tareas de limpieza (una por línea).")

    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nombre} ({self.codigo_barras})"

    class Meta:
        verbose_name = "Activo de Limpieza"
        verbose_name_plural = "Catálogo de Activos"


class RegistroLimpieza(models.Model):
    ESTADOS = [
        ('A TIEMPO', 'A Tiempo'),
        ('POR VENCER', 'Por Vencer'),
        ('VENCIDO', 'Vencido'),
    ]

    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    fecha_hora = models.DateTimeField(default=timezone.now)

    activo_relacionado = models.ForeignKey(ActivoLimpieza, on_delete=models.SET_NULL, null=True,
                                           related_name='registros')
    nombre_activo_snapshot = models.CharField(max_length=200)
    area_snapshot = models.CharField(max_length=100)

    tipo_limpieza = models.CharField(max_length=50, default="RUTINA", choices=[
        ('RUTINA', 'Rutina'), ('PROFUNDA', 'Profunda'), ('DESINFECCION', 'Desinfección')
    ])

    realizado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    verificado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                       related_name='verificaciones_limpieza')

    frecuencia_aplicada = models.IntegerField()
    proximo_vencimiento = models.DateTimeField(null=True, blank=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='A TIEMPO')

    # CAMBIO: Usamos TextField para guardar el historial como texto simple
    checklist_realizado = models.TextField(blank=True, default="")
    quimicos_usados = models.TextField(blank=True, default="")
    observaciones = models.TextField(blank=True, null=True)

    evidencia_pdf = models.FileField(upload_to='evidencias/limpieza/', null=True, blank=True)

    def __str__(self):
        return f"{self.fecha_hora.date()} - {self.nombre_activo_snapshot} - {self.estado}"

    class Meta:
        ordering = ['-fecha_hora']
        verbose_name = "Registro de Ejecución"
        verbose_name_plural = "Bitácora de Ejecuciones"