from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class RiesgoOportunidad(models.Model):
    TIPO_CHOICES = [
        ('RIESGO', 'Riesgo'),
        ('OPORTUNIDAD', 'Oportunidad'),
    ]

    ORIGEN_CHOICES = [
        ('AUDITORIA', 'Auditoría Interna/Externa'),
        ('REVISION_DIRECCION', 'Revisión por la Dirección'),
        ('TNC', 'Trabajo No Conforme'),
        ('QUEJA', 'Queja de Cliente'),
        ('OPERACION', 'Operación Diaria / Proceso'),
        ('CONTEXTO', 'Análisis de Contexto'),
    ]

    ESTADO_CHOICES = [
        ('IDENTIFICADO', 'Identificado'),
        ('PLANIFICACION', 'Planificación de Acciones'),
        ('IMPLEMENTACION', 'En Implementación'),
        ('EVALUACION', 'Evaluando Eficacia'),
        ('CERRADO', 'Cerrado'),
    ]

    NIVEL_CHOICES = [
        (1, 'Bajo (1)'),
        (2, 'Medio (2)'),
        (3, 'Alto (3)'),
    ]

    codigo_ro = models.CharField(max_length=50, unique=True, verbose_name="Código (Ej. RO-001)")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='RIESGO')
    origen = models.CharField(max_length=50, choices=ORIGEN_CHOICES)
    fecha_identificacion = models.DateField(default=timezone.now, verbose_name="Fecha de Identificación")
    descripcion = models.TextField(verbose_name="Descripción del Riesgo/Oportunidad")
    identificado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='ro_identificados')

    # ISO 17025 8.5.1: Matriz de Evaluación
    probabilidad = models.IntegerField(choices=NIVEL_CHOICES, default=1, verbose_name="Probabilidad")
    impacto = models.IntegerField(choices=NIVEL_CHOICES, default=1, verbose_name="Impacto")

    # ISO 17025 8.5.2: Acciones Planificadas
    acciones_planificadas = models.TextField(blank=True, verbose_name="Acciones Planificadas")
    responsable_accion = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='ro_responsables', verbose_name="Responsable de Implementación")
    fecha_limite = models.DateField(null=True, blank=True, verbose_name="Fecha Límite de Implementación")

    # ISO 17025 8.5.3: Evaluación de Eficacia
    evaluacion_eficacia = models.TextField(blank=True, verbose_name="Evaluación de la Eficacia de las Acciones")
    eficaz = models.BooleanField(default=False, verbose_name="¿Fueron eficaces las acciones?")
    fecha_cierre = models.DateTimeField(null=True, blank=True)

    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='IDENTIFICADO')
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Riesgo u Oportunidad"
        verbose_name_plural = "Riesgos y Oportunidades"

    @property
    def nivel_criticidad(self):
        """Calcula el nivel multiplicando Probabilidad x Impacto"""
        return self.probabilidad * self.impacto

    def __str__(self):
        return f"{self.codigo_ro} - {self.get_tipo_display()}"