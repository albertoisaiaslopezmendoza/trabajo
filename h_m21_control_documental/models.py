from django.db import models
from django.contrib.auth.models import User


class DocumentoSGC(models.Model):
    TIPO_CHOICES = [
        ('MANUAL', 'Manual'),
        ('PROCEDIMIENTO', 'Procedimiento'),
        ('INSTRUCTIVO', 'Instructivo de Trabajo'),
        ('FORMATO', 'Formato / Registro'),
        ('POLITICA', 'Política'),
        ('EXTERNO', 'Documento Externo / Norma'),
    ]

    ESTADO_CHOICES = [
        ('BORRADOR', 'Borrador / En Desarrollo'),
        ('REVISION', 'En Revisión'),
        ('APROBADO', 'Aprobado (Pendiente Publicación)'),
        ('VIGENTE', 'Vigente / Publicado'),
        ('OBSOLETO', 'Obsoleto / Retirado'),
    ]

    # ISO 17025 8.3.2 e): Identificación única
    codigo = models.CharField(max_length=50, verbose_name="Código del Documento")
    titulo = models.CharField(max_length=200, verbose_name="Título del Documento")
    tipo = models.CharField(max_length=30, choices=TIPO_CHOICES, default='PROCEDIMIENTO')

    # ISO 17025 8.3.2 c): Identificación de cambios y estado de revisión actual
    version = models.IntegerField(default=1, verbose_name="Versión Actual")
    descripcion_cambios = models.TextField(blank=True,
                                           verbose_name="Descripción de Cambios (Justificación de la nueva versión)")

    enlace_archivo = models.URLField(max_length=500, blank=True, verbose_name="Enlace al Archivo (Local o SharePoint)")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='BORRADOR')

    # ISO 17025 8.3.2 a) y b): Aprobación, revisión y actualización
    elaborado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='docs_elaborados')
    revisado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='docs_revisados')
    aprobado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                     related_name='docs_aprobados')

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_aprobacion = models.DateField(null=True, blank=True, verbose_name="Fecha de Aprobación")
    fecha_proxima_revision = models.DateField(null=True, blank=True,
                                              verbose_name="Fecha de Próxima Revisión Programada")

    class Meta:
        verbose_name = "Documento del SGC"
        verbose_name_plural = "Control Documental del SGC"
        # Garantiza que no haya dos versiones vigentes del mismo código
        unique_together = ('codigo', 'version')

    def __str__(self):
        return f"{self.codigo} - {self.titulo} (v{self.version})"