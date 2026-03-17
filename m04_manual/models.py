from django.db import models
from django.contrib.auth.models import User
from datetime import date


def add_months(d: date, months: int) -> date:
    """Suma meses a una fecha manteniendo día válido (Misma lógica original)."""
    y = d.year + (d.month - 1 + months) // 12
    m = (d.month - 1 + months) % 12 + 1
    dim = [31, 29 if (y % 4 == 0 and (y % 100 != 0 or y % 400 == 0)) else 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    day = min(d.day, dim[m - 1])
    return date(y, m, day)


class ManualSGC(models.Model):
    ESTADOS = [
        ('BORRADOR', 'Borrador'),
        ('APROBADO', 'Aprobado'),
        ('OBSOLETO', 'Obsoleto')
    ]

    doc_code = models.CharField("Código", max_length=50, default='SGC-DO-01')
    doc_title = models.CharField("Título", max_length=200, default='Manual de Calidad y Procesos')
    contenido = models.TextField("Contenido del Manual")
    version = models.CharField("Versión", max_length=20, default='1.0')
    estado = models.CharField("Estatus", max_length=20, choices=ESTADOS, default='BORRADOR')
    cambio_resumen = models.TextField("Resumen de Cambios", default='Creación inicial')

    elaborado_por = models.CharField("Elaborado por", max_length=150)
    aprobado_por = models.CharField("Aprobado por", max_length=150, blank=True, null=True)
    fecha = models.DateTimeField("Fecha Creación", auto_now_add=True)
    fecha_aprobacion = models.DateTimeField("Fecha Aprobación", blank=True, null=True)

    fecha_vigencia = models.DateField("Fecha de Vigencia", default=date.today)
    proxima_revision = models.DateField("Próxima Revisión", blank=True, null=True)

    def save(self, *args, **kwargs):
        # Calcular automáticamente la próxima revisión a 24 meses
        if self.fecha_vigencia and not self.proxima_revision:
            self.proxima_revision = add_months(self.fecha_vigencia, 24)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.doc_code} v{self.version} - {self.estado}"


class ManualDistribution(models.Model):
    TIPOS_COPIA = [
        ('CONTROLADA', 'Controlada'),
        ('NO CONTROLADA', 'No Controlada')
    ]

    manual = models.ForeignKey(ManualSGC, on_delete=models.CASCADE, related_name='distribuciones')
    recipient_name = models.CharField("Destinatario", max_length=150)
    area = models.CharField("Área", max_length=100, blank=True)
    copy_type = models.CharField("Tipo de Copia", max_length=50, choices=TIPOS_COPIA, default='CONTROLADA')
    delivery_method = models.CharField("Método de Entrega", max_length=100, blank=True)
    delivered_on = models.DateField("Fecha de Entrega", blank=True, null=True)
    ack_received = models.BooleanField("Acuse Recibido", default=False)
    ack_on = models.DateField("Fecha de Acuse", blank=True, null=True)

    created_by = models.CharField("Creado por", max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.recipient_name} - {self.copy_type}"