from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class AreaLaboratorio(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Área del Laboratorio")
    descripcion = models.TextField(blank=True, null=True)

    # Límites de Control
    temp_min_permitida = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Temp. Mínima (°C)")
    temp_max_permitida = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Temp. Máxima (°C)")
    humedad_min_permitida = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Humedad Mínima (%)")
    humedad_max_permitida = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Humedad Máxima (%)")

    class Meta:
        verbose_name = "Área de Laboratorio"
        verbose_name_plural = "Áreas de Laboratorio"

    def __str__(self):
        return self.nombre


class RegistroAmbiental(models.Model):
    area = models.ForeignKey(AreaLaboratorio, on_delete=models.CASCADE, related_name='registros')
    fecha_hora = models.DateTimeField(default=timezone.now, verbose_name="Fecha y Hora del Registro")

    temperatura = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Temperatura Registrada (°C)")
    humedad = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Humedad Registrada (%)")

    observaciones = models.TextField(blank=True, null=True,
                                     help_text="Anotar si hubo alguna desviación o equipo usado.")

    # Campos de control y Audit Trail
    cumple_criterio = models.BooleanField(default=True, editable=False, verbose_name="¿Dentro de especificación?")
    registrado_por = models.ForeignKey(User, on_delete=models.PROTECT, related_name='registros_ambientales')

    class Meta:
        verbose_name = "Registro Ambiental"
        verbose_name_plural = "Registros Ambientales"
        ordering = ['-fecha_hora']

    def save(self, *args, **kwargs):
        # Lógica ISO 17025: Validar automáticamente si está dentro de los límites
        temp_valida = self.area.temp_min_permitida <= self.temperatura <= self.area.temp_max_permitida
        humedad_valida = self.area.humedad_min_permitida <= self.humedad <= self.area.humedad_max_permitida

        self.cumple_criterio = temp_valida and humedad_valida
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.area.nombre} - {self.fecha_hora.strftime('%d/%m/%Y %H:%M')}"