from django.db import models
from django.contrib.auth.models import User
from e_m05_metodos_sops.models import MetodoSOP


class RegistroTecnico(models.Model):
    ESTADO_CHOICES = [
        ('EN_PROCESO', 'En Proceso (Borrador Editable)'),
        ('FINALIZADO', 'Finalizado (Bloqueado/Solo Lectura)'),
        ('REVISADO', 'Revisado por Calidad'),
    ]

    folio_registro = models.CharField(max_length=50, unique=True, verbose_name="Folio del Registro (Ej. RT-26-001)")
    identificador_muestra = models.CharField(max_length=100, verbose_name="Identificación de la Muestra / Ítem")
    metodo = models.ForeignKey(MetodoSOP, on_delete=models.PROTECT, verbose_name="Método de Ensayo o SOP")

    fecha_inicio = models.DateTimeField(verbose_name="Fecha y Hora de Inicio del Ensayo")
    fecha_fin = models.DateTimeField(null=True, blank=True, verbose_name="Fecha y Hora de Finalización")

    # Datos primarios y derivados (Cláusula 7.5 ISO 17025)
    datos_crudos = models.TextField(verbose_name="Observaciones Originales / Datos Crudos",
                                    help_text="Capture las lecturas directas del equipo. No modifique los datos posteriormente.")
    calculos_resultados = models.TextField(blank=True, null=True, verbose_name="Cálculos y Resultados Derivados")

    evidencia_adjunta = models.FileField(upload_to='registros_tecnicos/evidencias/', blank=True, null=True,
                                         verbose_name="Evidencia Adjunta (Imágenes, XLSX)")

    # Cumplimiento de Audit Trail y Responsabilidad
    analista = models.ForeignKey(User, on_delete=models.PROTECT, related_name='ensayos_m12_ejecutados',
                                 verbose_name="Analista Responsable")
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='EN_PROCESO')

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Registro Técnico (E_m12)"
        verbose_name_plural = "Registros Técnicos (E_m12)"
        ordering = ['-fecha_inicio']

    def __str__(self):
        return f"{self.folio_registro} - Muestra: {self.identificador_muestra}"