from django.db import models
from django.contrib.auth.models import User


class TrabajoNoConforme(models.Model):
    ESTADO_CHOICES = [
        ('REPORTADO', 'Reportado / Identificado'),
        ('EVALUACION', 'En Evaluación'),
        ('ACCION_TOMADA', 'Acciones Tomadas'),
        ('CERRADO', 'Cerrado'),
    ]

    IMPACTO_CHOICES = [
        ('BAJO', 'Bajo (Aceptable con desviación mínima)'),
        ('MEDIO', 'Medio (Requiere repetición o ajuste)'),
        ('ALTO', 'Alto (Afecta validez del resultado)'),
    ]

    codigo_tnc = models.CharField(max_length=50, unique=True, verbose_name="Código TNC (Ej. TNC-001)")
    fecha_identificacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Identificación")
    descripcion_no_conformidad = models.TextField(verbose_name="Descripción del Trabajo No Conforme")
    identificado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='tnc_identificados')

    # ISO 17025: 7.10.1 b) acciones tomadas (Ej. Detener trabajo, retener informe)
    acciones_inmediatas = models.TextField(blank=True, verbose_name="Acciones Inmediatas Tomadas")

    # ISO 17025: 7.10.1 c) evaluación de la importancia
    evaluacion_importancia = models.TextField(blank=True, verbose_name="Evaluación de la Importancia")
    impacto = models.CharField(max_length=20, choices=IMPACTO_CHOICES, default='BAJO')
    responsable_evaluacion = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                               related_name='tnc_evaluados',
                                               verbose_name="Responsable de la Evaluación")

    # ISO 17025: 7.10.1 d) y e) decisión de aceptabilidad y cliente
    decision_aceptabilidad = models.TextField(blank=True, verbose_name="Decisión sobre Aceptabilidad")
    requiere_notificar_cliente = models.BooleanField(default=False, verbose_name="¿Requiere Notificar al Cliente?")
    cliente_notificado = models.BooleanField(default=False, verbose_name="Cliente Notificado (Confirmación)")

    # ISO 17025: 7.10.1 f) autorización reanudar
    autoriza_reanudar = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                          related_name='tnc_autorizados',
                                          verbose_name="Autoriza Reanudación del Trabajo")
    fecha_reanudacion = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Reanudación")

    # ISO 17025: 7.10.3 Acciones correctivas (Se conecta con Cláusula 8.7)
    requiere_accion_correctiva = models.BooleanField(default=False, verbose_name="¿Genera Acción Correctiva?")

    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='REPORTADO')
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Trabajo No Conforme"
        verbose_name_plural = "Trabajos No Conformes"

    def __str__(self):
        return f"{self.codigo_tnc} - {self.get_estado_display()}"