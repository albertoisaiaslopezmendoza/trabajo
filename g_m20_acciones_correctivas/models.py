from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class AccionCorrectiva(models.Model):
    ORIGEN_CHOICES = [
        ('AUDITORIA_INTERNA', 'Auditoría Interna'),
        ('AUDITORIA_EXTERNA', 'Auditoría Externa'),
        ('TNC', 'Trabajo No Conforme'),
        ('QUEJA', 'Queja de Cliente'),
        ('REVISION_DIRECCION', 'Revisión por la Dirección'),
        ('OTRO', 'Otro / Mejora Continua'),
    ]

    ESTADO_CHOICES = [
        ('REGISTRADA', 'Registrada'),
        ('ANALISIS_CAUSA', 'Análisis de Causa Raíz'),
        ('IMPLEMENTACION', 'En Implementación'),
        ('EVALUACION', 'Evaluando Eficacia'),
        ('CERRADA', 'Cerrada'),
    ]

    codigo_ac = models.CharField(max_length=50, unique=True, verbose_name="Código (Ej. AC-001)")
    origen = models.CharField(max_length=50, choices=ORIGEN_CHOICES, verbose_name="Origen de la No Conformidad")
    referencia_origen = models.CharField(max_length=100, blank=True,
                                         verbose_name="Referencia (Ej. TNC-005, Informe Auditoría)")
    fecha_apertura = models.DateField(default=timezone.now, verbose_name="Fecha de Apertura")
    descripcion_no_conformidad = models.TextField(verbose_name="Descripción de la No Conformidad")
    reportado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='ac_reportadas')

    # ISO 17025 8.7.1 b): Análisis de Causa Raíz
    analisis_causa_raiz = models.TextField(blank=True,
                                           verbose_name="Análisis de Causa Raíz (Metodología usada ej. 5 Porqués)")

    # ISO 17025 8.7.1 c): Acciones Correctivas Implementadas
    acciones_implementadas = models.TextField(blank=True, verbose_name="Acciones Correctivas Implementadas")
    responsable_implementacion = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                                   related_name='ac_responsables',
                                                   verbose_name="Responsable de Implementación")
    fecha_limite_implementacion = models.DateField(null=True, blank=True, verbose_name="Fecha Límite de Implementación")

    # ISO 17025 8.7.1 d): Revisión de la eficacia
    evaluacion_eficacia = models.TextField(blank=True, verbose_name="Evaluación de la Eficacia")
    es_eficaz = models.BooleanField(default=False, verbose_name="¿La acción fue eficaz?")
    fecha_cierre = models.DateTimeField(null=True, blank=True, verbose_name="Fecha de Cierre")

    # ISO 17025 8.7.1 e): Actualización de riesgos y oportunidades
    requiere_actualizar_riesgos = models.BooleanField(default=False,
                                                      verbose_name="¿Requiere actualizar Riesgos/Oportunidades?")

    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='REGISTRADA')
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Acción Correctiva y Mejora"
        verbose_name_plural = "Acciones Correctivas y Mejoras"

    def __str__(self):
        return f"{self.codigo_ac} - {self.get_estado_display()}"