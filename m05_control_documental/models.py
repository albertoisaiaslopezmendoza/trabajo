from django.db import models


class DocumentoControlado(models.Model):
    # Campos base del Listado Maestro
    codigo = models.CharField(max_length=50, unique=True)
    titulo = models.CharField(max_length=255)
    tipo = models.CharField(max_length=100, default='Documento')
    area = models.CharField(max_length=100, blank=True)
    estado = models.CharField(max_length=50, default='Borrador')
    version = models.CharField(max_length=20, default='1.0')
    contenido = models.TextField(blank=True)
    cambios = models.TextField(blank=True)
    fecha = models.DateTimeField(auto_now=True)

    # Campos de flujo de aprobación y confidencialidad
    aprobacion_solicitado_por = models.CharField(max_length=100, blank=True, null=True)
    aprobacion_resuelto_por = models.CharField(max_length=100, blank=True, null=True)
    aprobacion_comentarios = models.TextField(blank=True, null=True)
    confidencialidad_2 = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"{self.codigo} - {self.titulo}"