from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Documento(models.Model):
    ESTADOS = [
        ('BORRADOR', 'Borrador'),
        ('VIGENTE', 'Vigente'),
        ('OBSOLETO', 'Obsoleto'),
    ]

    # Metadatos del documento
    codigo = models.CharField(max_length=50, unique=True)
    titulo = models.CharField(max_length=255)
    sistema = models.CharField(max_length=100, default='SGC ISO/IEC 17025')
    tipo_documento = models.CharField(max_length=50, choices=[
        ('Procedimiento', 'Procedimiento'),
        ('Instructivo', 'Instructivo'),
        ('Formato', 'Formato'),
        ('Manual', 'Manual'),
        ('Política', 'Política'),
        ('Plan', 'Plan')
    ])
    version = models.CharField(max_length=10, default='01')
    area = models.CharField(max_length=100)
    fecha_emision = models.DateField(default=timezone.now)
    vigencia_meses = models.IntegerField(default=24)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='BORRADOR')

    # Aprobaciones (Relacionamos con usuarios del sistema para SaaS)
    elaboro = models.ForeignKey(User, related_name='docs_elaboro', on_delete=models.SET_NULL, null=True, blank=True)
    fecha_firma_elaboro = models.DateField(null=True, blank=True)

    reviso = models.ForeignKey(User, related_name='docs_reviso', on_delete=models.SET_NULL, null=True, blank=True)
    fecha_firma_reviso = models.DateField(null=True, blank=True)

    aprobo = models.ForeignKey(User, related_name='docs_aprobo', on_delete=models.SET_NULL, null=True, blank=True)
    fecha_firma_aprobo = models.DateField(null=True, blank=True)

    # Contenido (TextField para almacenar texto largo)
    objetivo = models.TextField(blank=True)
    alcance = models.TextField(blank=True)
    responsabilidades = models.TextField(blank=True)
    definiciones = models.TextField(blank=True)
    procedimiento = models.TextField(blank=True)
    registros = models.TextField(blank=True)
    referencias = models.TextField(blank=True)
    anexos = models.TextField(blank=True)

    nota_control = models.TextField(
        default="Este documento es controlado. La versión vigente se encuentra disponible en el Sistema de Gestión del Laboratorio. Cualquier copia impresa se considera NO CONTROLADA.")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.codigo} - {self.titulo} (v{self.version})"

    class Meta:
        verbose_name = "Documento Controlado"
        verbose_name_plural = "Documentos Controlados"
        ordering = ['-created_at']


class CambioDocumento(models.Model):
    documento = models.ForeignKey(Documento, related_name='cambios', on_delete=models.CASCADE)
    revision = models.CharField(max_length=10)
    fecha = models.DateField(default=timezone.now)
    descripcion = models.TextField()
    elaboro = models.CharField(max_length=100)  # Texto libre o usuario
    aprobo = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Control de Cambio"


class DistribucionDocumento(models.Model):
    documento = models.ForeignKey(Documento, related_name='distribucion', on_delete=models.CASCADE)
    area = models.CharField(max_length=100)
    puesto = models.CharField(max_length=100)
    nombre = models.CharField(max_length=150, blank=True)
    copia_controlada = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Distribución"