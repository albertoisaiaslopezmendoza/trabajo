from django.db import models
from django.contrib.auth.models import User

# Clase base abstracta para cumplir con los requisitos de LABCOR
class AuditoriaBase(models.Model):
    id_registro = models.AutoField(primary_key=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)
    usuario_creacion = models.ForeignKey(User, related_name='%(class)s_creados', on_delete=models.SET_NULL, null=True, blank=True)
    usuario_modificacion = models.ForeignKey(User, related_name='%(class)s_modificados', on_delete=models.SET_NULL, null=True, blank=True)
    activo = models.BooleanField(default=True)

    class Meta:
        abstract = True

class Proveedor(AuditoriaBase):
    nombre = models.CharField(max_length=200, verbose_name="Nombre del Proveedor", unique=True)
    contacto = models.CharField(max_length=200, blank=True)
    telefono = models.CharField(max_length=50, blank=True)
    email = models.EmailField(blank=True)
    aprobado = models.BooleanField(default=False, verbose_name="Proveedor Aprobado")
    fecha_evaluacion = models.DateField(null=True, blank=True)
    comentarios = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

class Reactivo(AuditoriaBase):
    nombre = models.CharField(max_length=200)
    descripcion = models.TextField(blank=True, verbose_name="Descripción/Uso")
    ficha_seguridad = models.FileField(upload_to='m11/fichas_seguridad/', blank=True, null=True)
    proveedor = models.ForeignKey(Proveedor, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nombre

class LoteReactivo(AuditoriaBase):
    reactivo = models.ForeignKey(Reactivo, on_delete=models.CASCADE)
    numero_lote = models.CharField(max_length=100, verbose_name="Número de Lote")
    fecha_recepcion = models.DateField()
    fecha_caducidad = models.DateField()
    cantidad_recibida = models.DecimalField(max_digits=10, decimal_places=2)
    unidad_medida = models.CharField(max_length=50, help_text="Ej. L, ml, kg, g")
    certificado_analisis = models.FileField(upload_to='m11/certificados_lote/', blank=True, null=True)

    def __str__(self):
        return f"{self.reactivo.nombre} - Lote: {self.numero_lote}"

class AceptacionInsumo(AuditoriaBase):
    lote = models.ForeignKey(LoteReactivo, on_delete=models.CASCADE)
    fecha_evaluacion = models.DateField(auto_now_add=True)
    evaluador = models.CharField(max_length=100)
    cumple_especificaciones = models.BooleanField(default=False)
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f"Evaluación de: {self.lote}"

class ServicioExterno(AuditoriaBase):
    descripcion = models.CharField(max_length=200, help_text="Ej. Calibración de balanza")
    proveedor = models.ForeignKey(Proveedor, on_delete=models.CASCADE)
    fecha_servicio = models.DateField()
    certificado_servicio = models.FileField(upload_to='m11/servicios_externos/', blank=True, null=True)
    conforme = models.BooleanField(default=False, verbose_name="Servicio Conforme")

    def __str__(self):
        return self.descripcion