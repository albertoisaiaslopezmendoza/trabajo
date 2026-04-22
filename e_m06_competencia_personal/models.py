from django.db import models
from django.contrib.auth.models import User
from e_m05_metodos_sops.models import MetodoSOP


class Capacitacion(models.Model):
    TIPO_CHOICES = [
        ('INTERNA', 'Interna'),
        ('EXTERNA', 'Externa'),
        ('INDUCCION', 'Inducción al SGC'),
    ]
    ESTADO_CHOICES = [
        ('PROGRAMADA', 'Programada'),
        ('COMPLETADA', 'Completada'),
        ('VENCIDA', 'Vencida'),
    ]

    titulo = models.CharField(max_length=200, verbose_name="Nombre del Curso/Capacitación")
    empleado = models.ForeignKey(User, on_delete=models.CASCADE, related_name='capacitaciones_recibidas')
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    instructor = models.CharField(max_length=100)
    evidencia_pdf = models.FileField(upload_to='capacitaciones/evidencias/', blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='PROGRAMADA')

    creado_por = models.ForeignKey(User, on_delete=models.SET_NULL, null=True,
                                   related_name='capacitaciones_registradas')
    fecha_registro = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.titulo} - {self.empleado.get_full_name() or self.empleado.username}"


class AutorizacionMetodo(models.Model):
    personal = models.ForeignKey(User, on_delete=models.CASCADE, related_name='autorizaciones_metodos')
    metodo = models.ForeignKey(MetodoSOP, on_delete=models.CASCADE)
    fecha_autorizacion = models.DateField()
    autorizado_por = models.ForeignKey(User, on_delete=models.PROTECT, related_name='firmas_autorizacion')
    observaciones = models.TextField(blank=True, null=True)
    esta_activo = models.BooleanField(default=True, verbose_name="Autorización Vigente")

    class Meta:
        unique_together = ('personal', 'metodo')
        verbose_name = "Autorización de Método"
        verbose_name_plural = "Autorizaciones de Métodos"

    def __str__(self):
        return f"{self.personal.get_full_name() or self.personal.username} - {self.metodo.codigo}"