from django.db import models
from django.contrib.auth.models import User, Group

class PerfilPuesto(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Nombre del Puesto")
    # ISO 5.5 - Estructura organizacional y jerarquía
    reporta_a = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='subordinados', verbose_name="Reporta a")
    responsabilidades = models.TextField(verbose_name="Responsabilidades (ISO 5.5.b)")
    autoridades = models.TextField(verbose_name="Autoridades (ISO 5.5.c)")
    # ISO 6.2 - Competencia
    competencias_requeridas = models.TextField(verbose_name="Competencias Requeridas (ISO 6.2.2)")
    rol_sistema = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Rol en Sistema (RBAC)")

    class Meta:
        verbose_name = "Perfil de Puesto"
        verbose_name_plural = "Perfiles de Puesto"

    def __str__(self):
        return self.nombre

class PerfilEmpleado(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil_empleado')
    puesto = models.ForeignKey(PerfilPuesto, on_delete=models.RESTRICT, verbose_name="Perfil de Puesto")
    # Suplencias para garantizar continuidad de operaciones
    es_suplente_de = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='suplentes', verbose_name="Suplente autorizado de")
    firma_digital = models.ImageField(upload_to="firmas/", null=True, blank=True, verbose_name="Firma Digital")
    fecha_ingreso = models.DateField(verbose_name="Fecha de Ingreso")

    class Meta:
        verbose_name = "Perfil de Empleado"
        verbose_name_plural = "Perfiles de Empleados"

    def __str__(self):
        return f"{self.usuario.get_full_name()} - {self.puesto.nombre}"