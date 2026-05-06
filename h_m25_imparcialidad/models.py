# h_m25_imparcialidad/models.py
from django.db import models
from django.contrib.auth.models import User


class DeclaracionImparcialidad(models.Model):
    """Modelo para guardar las declaraciones firmadas por el personal."""

    # Agregamos related_name='declaraciones_m25' para evitar el choque con m00_imparcialidad
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='declaraciones_m25',
        verbose_name="Personal"
    )
    fecha_declaracion = models.DateField("Fecha de Declaración", auto_now_add=True)
    acepta_politicas = models.BooleanField("Acepto la Política de Imparcialidad", default=False)
    notas = models.TextField("Notas Adicionales", blank=True)

    def __str__(self):
        return f"Declaración de {self.usuario.username} - {self.fecha_declaracion}"

    # ... (Tus otros modelos, ConflictoInteres y Mitigacion, se quedan exactamente igual) ...
    def __str__(self):
        return f"Declaración de {self.usuario.username} - {self.fecha_declaracion}"

class ConflictoInteres(models.Model):
    """Modelo para registrar riesgos a la imparcialidad o conflictos de interés."""
    NIVEL_RIESGO = [
        ('BAJO', 'Bajo'),
        ('MEDIO', 'Medio'),
        ('ALTO', 'Alto'),
    ]
    ESTATUS_CHOICES = [
        ('ABIERTO', 'Abierto'),
        ('MITIGADO', 'Mitigado'),
    ]

    usuario_reporta = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Reportado por")
    fecha_reporte = models.DateField("Fecha de Reporte", auto_now_add=True)
    descripcion = models.TextField("Descripción del Riesgo/Conflicto")
    nivel_riesgo = models.CharField("Nivel de Riesgo", max_length=10, choices=NIVEL_RIESGO, default='BAJO')
    estatus = models.CharField("Estatus", max_length=15, choices=ESTATUS_CHOICES, default='ABIERTO')

    def __str__(self):
        return f"Riesgo {self.id} - {self.get_nivel_riesgo_display()}"

class Mitigacion(models.Model):
    """Modelo para dar seguimiento a las medidas de mitigación aplicadas."""
    conflicto = models.ForeignKey(ConflictoInteres, on_delete=models.CASCADE, related_name='mitigaciones', verbose_name="Conflicto Relacionado")
    descripcion_medida = models.TextField("Medida de Mitigación Aplicada")
    fecha_implementacion = models.DateField("Fecha de Implementación")
    responsable = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, verbose_name="Responsable")

    def __str__(self):
        return f"Mitigación para Conflicto {self.conflicto.id}"