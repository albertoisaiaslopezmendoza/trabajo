from django.db import models
from django.contrib.auth.models import User


class Muestra(models.Model):
    codigo = models.CharField(max_length=50, unique=True, verbose_name="Código de Muestra")
    descripcion = models.TextField(verbose_name="Descripción del ítem")
    metodo_muestreo = models.CharField(max_length=200, verbose_name="Método de Muestreo (Ref. Documental)")
    fecha_muestreo = models.DateTimeField(verbose_name="Fecha y Hora de Muestreo")
    condiciones_ambientales = models.CharField(max_length=200, blank=True, null=True, help_text="Ej: 25°C, 45% HR")
    responsable_muestreo = models.CharField(max_length=100, verbose_name="Realizado por")

    # Audit Trail
    activo = models.BooleanField(default=True)
    usuario_creacion = models.ForeignKey(User, on_delete=models.PROTECT)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.codigo


class CadenaCustodia(models.Model):
    muestra = models.ForeignKey(Muestra, on_delete=models.CASCADE, related_name="custodias")
    fecha_transferencia = models.DateTimeField(auto_now_add=True)
    entregado_por = models.CharField(max_length=100)
    recibido_por = models.CharField(max_length=100)
    comentarios = models.TextField(blank=True, null=True)

    # Audit Trail
    usuario_creacion = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return f"Custodia {self.muestra.codigo} - {self.fecha_transferencia.strftime('%d/%m/%Y')}"