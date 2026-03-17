import uuid
import hashlib
import json
from django.db import models
from django.conf import settings
from django.utils import timezone


class DeclaracionImparcialidad(models.Model):
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    # Datos del firmante
    nombre_completo = models.CharField(max_length=200)
    puesto = models.CharField(max_length=200)
    area = models.CharField(max_length=200, blank=True)

    # Aceptaciones
    acepta_imparcialidad = models.BooleanField(default=False)
    acepta_confidentialidad = models.BooleanField(default=False)
    acepta_privacidad = models.BooleanField(default=False)

    observaciones = models.TextField(blank=True, null=True)

    # Firma: Guardamos la imagen generada por Python o subida por el usuario
    firma_imagen = models.ImageField(upload_to='firmas_m00/', verbose_name="Imagen de Firma")

    # Integridad (Blockchain simple)
    prev_hash = models.CharField(max_length=64, verbose_name="Hash Anterior")
    hash_registro = models.CharField(max_length=64, verbose_name="Hash Evidencia")

    created_at = models.DateTimeField(auto_now_add=True)
    ip_origen = models.GenericIPAddressField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Declaración M00"

    def calcular_hash(self, secret_key="LIMS_SECRET"):
        """Calcula hash SHA256 usando metadatos y la ruta de la firma"""
        payload = {
            "uid": self.usuario.id,
            "nombre": self.nombre_completo,
            "fecha": str(self.created_at),
            "prev": self.prev_hash,
            "firma_path": str(self.firma_imagen.name)
        }
        # Crear string único
        raw = f"{secret_key}|{json.dumps(payload, sort_keys=True)}"
        return hashlib.sha256(raw.encode()).hexdigest()