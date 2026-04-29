from django.db import models
from django.contrib.auth.models import User


class InformeCertificado(models.Model):  # Corregido: models.Model en lugar de models.models
    ESTADO_CHOICES = [
        ('BORRADOR', 'Borrador'),
        ('REVISION', 'En Revisión'),
        ('APROBADO', 'Aprobado'),
        ('EMITIDO', 'Emitido'),
        ('CANCELADO', 'Cancelado / Modificado'),
    ]

    TIPO_CHOICES = [
        ('ENSAYO', 'Informe de Ensayo'),
        ('CALIBRACION', 'Certificado de Calibración'),
    ]

    codigo_informe = models.CharField(max_length=50, unique=True, verbose_name="Código del Informe")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, verbose_name="Tipo de Documento")

    fecha_emision = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Emisión")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='BORRADOR')

    declaracion_conformidad = models.TextField(blank=True, verbose_name="Declaración de Conformidad")
    opiniones_interpretaciones = models.TextField(blank=True, verbose_name="Opiniones e Interpretaciones")

    # --- NUEVOS CAMPOS PARA ISO 17025 (Enmiendas 7.8.8) ---
    es_enmienda = models.BooleanField(default=False, verbose_name="Es una enmienda")
    informe_original = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                         related_name='enmiendas_generadas')
    # ------------------------------------------------------

    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='informes_creados')
    revisado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='informes_revisados')
    aprobado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='informes_aprobados')

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Informe / Certificado"
        verbose_name_plural = "Informes y Certificados"

    def __str__(self):
        return f"{self.codigo_informe} - {self.get_estado_display()}"