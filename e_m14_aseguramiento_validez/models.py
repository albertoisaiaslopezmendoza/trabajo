from django.db import models
from django.contrib.auth.models import User
from e_m05_metodos_sops.models import MetodoSOP
from e_m12_ejecucion_registros.models import RegistroTecnico


class RegistroQC(models.Model):
    TIPO_QC_CHOICES = [
        ('BLANCO', 'Blanco de Reactivo / Muestra'),
        ('DUPLICADO', 'Duplicado de Ensayo'),
        ('MRC', 'Material de Referencia Certificado'),
        ('CIEGO', 'Muestra Ciega'),
        ('PT', 'Ensayo de Aptitud (Proficiency Testing)'),
    ]
    ESTADO_CHOICES = [
        ('EN_PROCESO', 'En Proceso (Editable)'),
        ('FINALIZADO', 'Finalizado (Bloqueado/Inmutable)'),
    ]

    folio_qc = models.CharField(max_length=50, unique=True, verbose_name="Folio de Control (Ej. QC-2026-001)")
    metodo = models.ForeignKey(MetodoSOP, on_delete=models.PROTECT, verbose_name="Método Evaluado")

    # Puede estar ligado a un registro de muestras específico, o ser independiente (como un PT anual)
    registro_tecnico_asociado = models.ForeignKey(RegistroTecnico, on_delete=models.SET_NULL, null=True, blank=True,
                                                  related_name='controles_calidad',
                                                  help_text="Opcional: Lote de muestras asociado")

    tipo_control = models.CharField(max_length=20, choices=TIPO_QC_CHOICES)
    fecha_ejecucion = models.DateField(verbose_name="Fecha de Ejecución del Control")

    # ISO 17025 Cláusula 7.7
    criterios_aceptacion = models.TextField(verbose_name="Criterios de Aceptación (Límites permitidos)")
    resultados_obtenidos = models.TextField(verbose_name="Resultados Obtenidos (Datos crudos QC)")
    es_conforme = models.BooleanField(default=True, verbose_name="¿El control es Conforme?")

    evidencia_adjunta = models.FileField(upload_to='qc_evidencias/', blank=True, null=True,
                                         verbose_name="Evidencia Adjunta (Cartas de Control, Reportes PT)")

    # Trazabilidad y Seguridad (Rúbricas)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='EN_PROCESO')
    analista = models.ForeignKey(User, on_delete=models.PROTECT, related_name='controles_realizados')
    fecha_registro = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Registro de Aseguramiento de Validez"
        verbose_name_plural = "Registros de Aseguramiento de Validez"
        ordering = ['-fecha_ejecucion']

    def __str__(self):
        return f"{self.folio_qc} - {self.get_tipo_control_display()} ({self.metodo.codigo})"