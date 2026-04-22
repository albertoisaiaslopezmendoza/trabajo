from django.db import models
from django.contrib.auth.models import User


class MetodoSOP(models.Model):
    TIPO_CHOICES = [
        ('METODO', 'Método de Ensayo'),
        ('SOP', 'Procedimiento Operativo Estándar (SOP)'),
        ('INSTRUCTIVO', 'Instructivo de Trabajo'),
    ]
    ESTADO_CHOICES = [
        ('VIGENTE', 'Vigente'),
        ('EN_REVISION', 'En Revisión'),
        ('OBSOLETO', 'Obsoleto'),
    ]

    codigo = models.CharField(max_length=50, unique=True, verbose_name="Código del Documento")
    titulo = models.CharField(max_length=200, verbose_name="Título del Método / SOP")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='METODO')
    version = models.CharField(max_length=10, verbose_name="Versión Actual")

    fecha_emision = models.DateField(verbose_name="Fecha de Emisión")
    fecha_proxima_revision = models.DateField(verbose_name="Próxima Revisión")

    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='VIGENTE')

    archivo_pdf = models.FileField(upload_to='metodos_sops/', blank=True, null=True, verbose_name="Documento (PDF)")

    # Audit Trail Básico
    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='metodos_creados')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Método o SOP"
        verbose_name_plural = "Métodos y SOPs"
        ordering = ['-estado', 'codigo']

    def __str__(self):
        return f"{self.codigo} - {self.titulo} (v{self.version})"


class ValidacionVerificacion(models.Model):
    metodo = models.ForeignKey(MetodoSOP, on_delete=models.CASCADE, related_name='validaciones')
    fecha_aprobacion = models.DateField(verbose_name="Fecha de Aprobación de la Validación/Verificación")
    responsable = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    reporte_evidencia = models.FileField(upload_to='validaciones_metodos/', blank=True, null=True)
    comentarios = models.TextField(blank=True, null=True)

    class Meta:
        verbose_name = "Validación/Verificación"
        verbose_name_plural = "Validaciones/Verificaciones"

    def __str__(self):
        return f"Validación de {self.metodo.codigo} - {self.fecha_aprobacion}"