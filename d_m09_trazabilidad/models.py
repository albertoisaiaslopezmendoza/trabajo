from django.db import models
from django.contrib.auth.models import User


class MaterialReferencia(models.Model):
    ESTADOS = [
        ('VIGENTE', 'Vigente / Apto para uso'),
        ('CUARENTENA', 'En Cuarentena'),
        ('AGOTADO', 'Agotado / Consumido'),
        ('CADUCADO', 'Caducado / Fuera de uso'),
    ]

    codigo_interno = models.CharField(max_length=50, unique=True, verbose_name="ID Interno (Ej: MRC-001)")
    nombre = models.CharField(max_length=150, verbose_name="Descripción del Material")
    marca_fabricante = models.CharField(max_length=100, verbose_name="Fabricante / Instituto (Ej: NIST, CENAM)")
    lote = models.CharField(max_length=50, verbose_name="Lote No.")
    certificado_numero = models.CharField(max_length=100, verbose_name="No. de Certificado")
    incertidumbre = models.CharField(max_length=100, verbose_name="Valor de Incertidumbre y Cobertura (k=2)")

    fecha_recepcion = models.DateField()
    fecha_apertura = models.DateField(blank=True, null=True)
    fecha_caducidad = models.DateField()

    ubicacion = models.CharField(max_length=100, help_text="Ej: Refrigerador 2, Gaveta A")
    condiciones_almacenamiento = models.CharField(max_length=150, help_text="Ej: 2 a 8 °C, Proteger de la luz")

    estado = models.CharField(max_length=20, choices=ESTADOS, default='VIGENTE')
    archivo_certificado = models.FileField(upload_to='certificados_mrc/', blank=True, null=True)

    # Audit Trail
    usuario_creacion = models.ForeignKey(User, on_delete=models.PROTECT)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.codigo_interno} - {self.nombre} (Lote: {self.lote})"


class UsoMaterial(models.Model):
    material = models.ForeignKey(MaterialReferencia, on_delete=models.CASCADE, related_name='usos')
    fecha_uso = models.DateTimeField(auto_now_add=True)
    motivo_uso = models.CharField(max_length=200, help_text="Ej: Verificación de balanza LABCOR-EQ-002, Ensayo X")
    cantidad_utilizada = models.CharField(max_length=50, help_text="Ej: 5 ml, 1 ampolleta")
    observaciones = models.TextField(blank=True, null=True)

    # Audit Trail (ISO 17025: ¿Quién lo usó?)
    usuario_registro = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return f"Uso de {self.material.codigo_interno} el {self.fecha_uso.strftime('%d/%m/%Y')}"