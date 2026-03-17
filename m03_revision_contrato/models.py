import uuid
import hashlib
from django.db import models
from django.utils import timezone


# Modelo auxiliar para simular la tabla sgc_quotes del original
class Cotizacion(models.Model):
    folio = models.CharField(max_length=50, unique=True, verbose_name="Folio Cotización")
    cliente = models.CharField(max_length=200)
    ensayo = models.CharField(max_length=200)
    norma = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.folio} - {self.cliente}"

    class Meta:
        verbose_name = "Cotización"
        verbose_name_plural = "Cotizaciones"


class RevisionContrato(models.Model):
    ESTADOS = [
        ('BORRADOR', 'Borrador'),
        ('APROBADO', 'Aprobado'),
        ('RECHAZADO', 'Rechazado'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Relación con cotización (en el original era solo texto, aquí lo hacemos relación para integridad)
    cotizacion = models.ForeignKey(Cotizacion, on_delete=models.CASCADE, related_name='revisiones')

    revision_no = models.PositiveIntegerField()
    fecha_revision = models.DateTimeField(default=timezone.now)
    fecha_aprobacion = models.DateTimeField(null=True, blank=True)

    # Datos copiados de la cotización para historial (snapshot)
    cliente = models.CharField(max_length=200)
    ensayo = models.CharField(max_length=200)
    norma = models.CharField(max_length=200)

    estado = models.CharField(max_length=20, choices=ESTADOS, default='BORRADOR')

    # Checklist ISO 17025 (7.1)
    alcance_confirmado = models.BooleanField(default=False, verbose_name="Alcance definido")
    capacidad_laboratorio = models.BooleanField(default=False, verbose_name="Capacidad técnica")
    recursos_disponibles = models.BooleanField(default=False, verbose_name="Recursos disponibles")
    metodo_validado = models.BooleanField(default=False, verbose_name="Método validado")
    incertidumbre_conocida = models.BooleanField(default=False, verbose_name="Incertidumbre conocida")
    plazo_aceptado = models.BooleanField(default=False, verbose_name="Plazo aceptado")
    revision_previa_ok = models.BooleanField(default=False, verbose_name="Revisión previa")

    cambios_detectados = models.BooleanField(default=False, verbose_name="¿Cambios al contrato?")
    descripcion_cambios = models.TextField(blank=True, null=True, verbose_name="Descripción de cambios")

    aprobado = models.BooleanField(default=False)
    aprobado_por = models.CharField(max_length=150)
    observaciones = models.TextField(blank=True, null=True)

    hash_registro = models.CharField(max_length=64, blank=True)

    def save(self, *args, **kwargs):
        # Lógica para calcular el número de revisión si es nuevo
        if not self.pk or self.revision_no is None:
            last_rev = RevisionContrato.objects.filter(cotizacion=self.cotizacion).order_by('-revision_no').first()
            if last_rev:
                self.revision_no = last_rev.revision_no + 1
            else:
                self.revision_no = 1

        # Generar Hash (Lógica traída del original)
        # folio|rev|estado|usuario
        raw_str = f"{self.cotizacion.folio}|{self.revision_no}|{self.estado}|{self.aprobado_por}"
        self.hash_registro = hashlib.sha256(raw_str.encode()).hexdigest()

        if self.estado == 'APROBADO' and not self.fecha_aprobacion:
            self.fecha_aprobacion = timezone.now()

        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-fecha_revision']