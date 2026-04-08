from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Equipo(models.Model):
    ESTADOS = [
        ('OPERATIVO', 'Operativo / Apto para uso'),
        ('CALIBRACION', 'En Proceso de Calibración'),
        ('MANTENIMIENTO', 'En Mantenimiento'),
        ('FUERA_SERVICIO', 'Fuera de Servicio / No Conforme'),
        ('BAJA', 'Baja Definitiva'),
    ]

    codigo_interno = models.CharField(max_length=50, unique=True, verbose_name="ID Interno (Ej: LABCOR-EQ-001)")
    nombre = models.CharField(max_length=100)
    marca = models.CharField(max_length=100)
    modelo = models.CharField(max_length=100)
    serie = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=100, help_text="Ej: Área de Corrosión, Lab B")
    fecha_ingreso = models.DateField(verbose_name="Fecha de Compra/Ingreso")
    estado = models.CharField(max_length=20, choices=ESTADOS, default='OPERATIVO')

    # Audit Trail
    usuario_creacion = models.ForeignKey(User, on_delete=models.PROTECT)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.codigo_interno} - {self.nombre}"


class Mantenimiento(models.Model):
    TIPOS = [('PREV', 'Preventivo'), ('CORR', 'Correctivo')]
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='mantenimientos')
    fecha_servicio = models.DateField()
    tipo = models.CharField(max_length=4, choices=TIPOS)
    descripcion = models.TextField(verbose_name="Detalles de la intervención")
    proximo_mantenimiento = models.DateField()
    realizado_por = models.CharField(max_length=100, help_text="Empresa externa o técnico interno")

    # Audit Trail
    usuario_registro = models.ForeignKey(User, on_delete=models.PROTECT)


class Calibracion(models.Model):
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='calibraciones')
    fecha_calibracion = models.DateField()
    proxima_calibracion = models.DateField()
    certificado_numero = models.CharField(max_length=50, verbose_name="Número de Certificado")
    resultado = models.CharField(max_length=100, help_text="Ej: Dentro de tolerancia / Incertidumbre +/- 0.1")
    conforme = models.BooleanField(default=True)
    archivo_certificado = models.FileField(upload_to='certificados_calibracion/', blank=True, null=True)

    # Audit Trail
    usuario_registro = models.ForeignKey(User, on_delete=models.PROTECT)