from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class RegistroCalidad(models.Model):
    TIPO_CHOICES = [
        ('TECNICO', 'Registro Técnico (Ensayos, Calibraciones)'),
        ('CALIDAD', 'Registro de Calidad (Auditorías, Revisiones)'),
        ('ADMINISTRATIVO', 'Registro Administrativo / Legal'),
    ]

    MEDIO_CHOICES = [
        ('FISICO', 'Físico (Papel / Carpeta)'),
        ('DIGITAL', 'Digital (Servidor / Nube)'),
        ('HIBRIDO', 'Híbrido (Ambos)'),
    ]

    ESTADO_CHOICES = [
        ('ACTIVO', 'Vigente / Activo'),
        ('ARCHIVADO', 'Archivado (Retención en progreso)'),
        ('DESTRUIDO', 'Destruido / Eliminado Seguro'),
    ]

    DISPOSICION_CHOICES = [
        ('DESTRUCCION_FISICA', 'Destrucción Física (Triturado)'),
        ('BORRADO_SEGURO', 'Borrado Seguro de Datos'),
        ('ARCHIVO_PERMANENTE', 'Archivo Muerto Permanente'),
    ]

    # ISO 17025 8.4.2: Identificación y Almacenamiento
    codigo_registro = models.CharField(max_length=50, unique=True, verbose_name="Código del Registro")
    titulo = models.CharField(max_length=200, verbose_name="Nombre o Título del Registro")
    tipo = models.CharField(max_length=30, choices=TIPO_CHOICES, default='CALIDAD')
    medio_almacenamiento = models.CharField(max_length=20, choices=MEDIO_CHOICES, default='DIGITAL')
    ubicacion_almacenamiento = models.CharField(max_length=200, verbose_name="Ubicación Física o Ruta Lógica")
    metodo_proteccion = models.CharField(max_length=200, default='Acceso restringido por rol y respaldos automatizados',
                                         verbose_name="Método de Protección")

    # ISO 17025 8.4.2: Tiempo de retención y disposición
    tiempo_retencion_anios = models.PositiveIntegerField(default=5, verbose_name="Tiempo de Retención (Años)")
    metodo_disposicion = models.CharField(max_length=30, choices=DISPOSICION_CHOICES, default='BORRADO_SEGURO')

    # Responsabilidades y Trazabilidad
    responsable_custodia = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                             related_name='registros_custodiados')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='ACTIVO')

    fecha_creacion_registro = models.DateField(default=timezone.now, verbose_name="Fecha de Generación del Registro")
    fecha_archivo = models.DateField(null=True, blank=True, verbose_name="Fecha en que se Archivó")
    fecha_destruccion = models.DateField(null=True, blank=True, verbose_name="Fecha de Destrucción / Eliminación")

    observaciones = models.TextField(blank=True, verbose_name="Observaciones / Evidencia de Destrucción")
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Control de Registro"
        verbose_name_plural = "Control de Registros"

    def __str__(self):
        return f"{self.codigo_registro} - {self.titulo}"