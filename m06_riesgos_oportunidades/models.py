from django.db import models

class RiesgoOportunidad(models.Model):
    TIPO_CHOICES = [
        ('Riesgo', 'Riesgo'),
        ('Oportunidad', 'Oportunidad')
    ]
    ESTADO_CHOICES = [
        ('Abierto', 'Abierto'),
        ('En progreso', 'En progreso'),
        ('Cerrado', 'Cerrado')
    ]

    proceso = models.CharField(max_length=200, verbose_name="Proceso")
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES, default='Riesgo')
    descripcion = models.TextField(verbose_name="Descripción")
    causa = models.TextField(blank=True, null=True)
    consecuencia = models.TextField(blank=True, null=True)
    control_actual = models.TextField(blank=True, null=True, verbose_name="Control Actual")
    accion_plan = models.TextField(blank=True, null=True, verbose_name="Acción Planificada")
    responsable = models.CharField(max_length=150, blank=True, null=True)
    fecha_objetivo = models.DateField(blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Abierto')
    probabilidad = models.IntegerField(default=1, verbose_name="Probabilidad (1-5)")
    impacto = models.IntegerField(default=1, verbose_name="Impacto (1-5)")
    evidencia = models.TextField(blank=True, null=True)
    creado_por = models.CharField(max_length=100, blank=True, null=True)
    revisado_por = models.CharField(max_length=100, blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    # Replicamos la lógica de cálculo que tenías en la app de escritorio
    @property
    def nivel(self):
        return self.probabilidad * self.impacto

    @property
    def clasificacion(self):
        if self.nivel >= 16:
            return "Crítico"
        if self.nivel >= 9:
            return "Alto"
        if self.nivel >= 4:
            return "Medio"
        return "Bajo"

    def __str__(self):
        return f"{self.tipo} - {self.proceso} ({self.clasificacion})"

class FirmaRiesgo(models.Model):
    riesgo = models.ForeignKey(RiesgoOportunidad, on_delete=models.CASCADE, related_name='firmas')
    nombre = models.CharField(max_length=150, blank=True, null=True)
    rol = models.CharField(max_length=100, default='Revisión/Aprobación')
    # En la web, guardaremos la firma como imagen en lugar de BYTEA puro
    firma_imagen = models.ImageField(upload_to='firmas_m06/', blank=True, null=True)
    creado_en = models.DateTimeField(auto_now_add=True)