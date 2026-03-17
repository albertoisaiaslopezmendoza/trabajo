from django.db import models


class AccionCorrectiva(models.Model):
    FUENTE_CHOICES = [
        ('Interna', 'Interna'), ('Cliente', 'Cliente'),
        ('Auditoría', 'Auditoría'), ('Proveedor', 'Proveedor'),
        ('Ensayo', 'Ensayo'), ('Otro', 'Otro')
    ]
    TIPO_CHOICES = [
        ('No Conformidad', 'No Conformidad'), ('Queja', 'Queja'),
        ('Hallazgo', 'Hallazgo'), ('Observación', 'Observación')
    ]
    SEVERIDAD_CHOICES = [
        ('Baja', 'Baja'), ('Media', 'Media'),
        ('Alta', 'Alta'), ('Crítica', 'Crítica')
    ]
    ESTADO_CHOICES = [
        ('Abierto', 'Abierto'), ('En progreso', 'En progreso'),
        ('Verificación', 'Verificación'), ('Cerrado', 'Cerrado')
    ]

    codigo = models.CharField(max_length=50, blank=True, null=True, verbose_name="Código")
    fuente = models.CharField(max_length=50, choices=FUENTE_CHOICES, default='Interna')
    tipo = models.CharField(max_length=50, choices=TIPO_CHOICES, default='No Conformidad')
    proceso = models.CharField(max_length=150)
    severidad = models.CharField(max_length=20, choices=SEVERIDAD_CHOICES, default='Media')
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Abierto')
    responsable = models.CharField(max_length=150, blank=True, null=True)
    fecha_objetivo = models.DateField(blank=True, null=True)
    creado_por = models.CharField(max_length=150, blank=True, null=True)
    revisado_por = models.CharField(max_length=150, blank=True, null=True)

    descripcion = models.TextField(verbose_name="Descripción (qué pasó)")
    evidencia = models.TextField(blank=True, null=True, verbose_name="Evidencia / Referencia")
    contencion = models.TextField(blank=True, null=True, verbose_name="Contención (acción inmediata)")
    correccion = models.TextField(blank=True, null=True, verbose_name="Corrección")

    # 5-Why
    why1 = models.CharField(max_length=255, blank=True, null=True, verbose_name="Why 1")
    why2 = models.CharField(max_length=255, blank=True, null=True, verbose_name="Why 2")
    why3 = models.CharField(max_length=255, blank=True, null=True, verbose_name="Why 3")
    why4 = models.CharField(max_length=255, blank=True, null=True, verbose_name="Why 4")
    why5 = models.CharField(max_length=255, blank=True, null=True, verbose_name="Why 5 (Causa raíz)")
    causa_raiz = models.CharField(max_length=255, blank=True, null=True)

    accion_correctiva = models.TextField(blank=True, null=True, verbose_name="Acción correctiva (plan)")
    verificacion = models.TextField(blank=True, null=True, verbose_name="Verificación")
    eficacia = models.TextField(blank=True, null=True, verbose_name="Eficacia")

    fecha_cierre = models.DateField(blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)

    # Para la firma, por simplicidad guardaremos la ruta de la imagen o un campo base64
    firma = models.TextField(blank=True, null=True, verbose_name="Firma Base64")

    def save(self, *args, **kwargs):
        # Auto-calcula la causa raíz tomando el último "Why" ingresado, igual que tu código original
        self.causa_raiz = self.why5 or self.why4 or self.why3 or self.why2 or self.why1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.codigo} - {self.proceso}"