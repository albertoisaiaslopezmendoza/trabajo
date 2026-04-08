from django.db import models
from django.contrib.auth.models import User
from c_m03_muestreo.models import Muestra  # Importante para la trazabilidad


class RecepcionMuestra(models.Model):
    ESTADOS = [
        ('RECIBIDA', 'Recibida en Laboratorio'),
        ('PROCESO', 'En Análisis / Ensayo'),
        ('RETORNADA', 'Retornada al Cliente'),
        ('DESECHADA', 'Desechada / Eliminada'),
    ]

    muestra = models.OneToOneField(Muestra, on_delete=models.CASCADE, related_name='recepcion')
    fecha_recepcion = models.DateTimeField(auto_now_add=True)
    conforme = models.BooleanField(default=True, verbose_name="¿Muestra cumple requisitos de ingreso?")
    observaciones_integridad = models.TextField(blank=True,
                                                help_text="Describa anomalías o desviaciones (ISO 17025: 7.4.2)")

    # Almacenamiento
    ubicacion_fisica = models.CharField(max_length=100, help_text="Ej: Refri 01, Estante B4")
    condiciones_almacenamiento = models.CharField(max_length=200, help_text="Ej: Mantener a 4°C, Proteger de la luz")
    estado_actual = models.CharField(max_length=20, choices=ESTADOS, default='RECIBIDA')

    # Audit Trail
    usuario_recepcion = models.ForeignKey(User, on_delete=models.PROTECT)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Rec: {self.muestra.codigo} - {self.estado_actual}"


class HistorialManejo(models.Model):
    recepcion = models.ForeignKey(RecepcionMuestra, on_delete=models.CASCADE, related_name='movimientos')
    fecha_movimiento = models.DateTimeField(auto_now_add=True)
    accion = models.CharField(max_length=100, help_text="Ej: Movida a zona de desecho, Iniciado análisis")
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)

    class Meta:
        verbose_name_plural = "Historial de Manejo de Muestras"