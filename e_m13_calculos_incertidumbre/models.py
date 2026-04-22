from django.db import models
from django.contrib.auth.models import User
from e_m05_metodos_sops.models import MetodoSOP
from e_m12_ejecucion_registros.models import RegistroTecnico


class PresupuestoIncertidumbre(models.Model):
    """Define el modelo matemático aprobado para calcular la incertidumbre de un ensayo"""
    metodo = models.ForeignKey(MetodoSOP, on_delete=models.CASCADE, related_name='presupuestos_incertidumbre')
    version = models.CharField(max_length=10, verbose_name="Versión del Presupuesto")
    fecha_aprobacion = models.DateField(auto_now_add=True)

    # Parámetros del modelo matemático ISO (GUM)
    descripcion_modelo = models.TextField(verbose_name="Descripción de fuentes (Tipo A y B)")
    factor_cobertura = models.DecimalField(max_digits=4, decimal_places=2, default=2.00,
                                           verbose_name="Factor k (95% confianza)")
    formula_aplicada = models.TextField(help_text="Fórmula para el cálculo combinado", blank=True)

    es_vigente = models.BooleanField(default=True)
    aprobado_por = models.ForeignKey(User, on_delete=models.PROTECT, related_name='presupuestos_aprobados')

    class Meta:
        verbose_name = "Presupuesto de Incertidumbre"
        verbose_name_plural = "Presupuestos de Incertidumbre"
        unique_together = ('metodo', 'version')

    def __str__(self):
        return f"Presupuesto {self.metodo.codigo} (v{self.version})"


class CalculoIncertidumbre(models.Model):
    """El registro instanciado del cálculo por un analista para un ensayo específico"""
    registro_tecnico = models.OneToOneField(RegistroTecnico, on_delete=models.CASCADE,
                                            related_name='calculo_incertidumbre')
    presupuesto_utilizado = models.ForeignKey(PresupuestoIncertidumbre, on_delete=models.PROTECT)

    # Datos de resultado (Derivados)
    resultado_medicion = models.DecimalField(max_digits=15, decimal_places=4,
                                             verbose_name="Resultado de la Medición (y)")
    incertidumbre_combinada = models.DecimalField(max_digits=15, decimal_places=6,
                                                  verbose_name="Incertidumbre Combinada (uc)")
    incertidumbre_expandida = models.DecimalField(max_digits=15, decimal_places=6,
                                                  verbose_name="Incertidumbre Expandida (U)")
    unidades = models.CharField(max_length=20, default="N/A")

    # Audit Trail
    calculado_por = models.ForeignKey(User, on_delete=models.PROTECT, related_name='calculos_realizados')
    fecha_calculo = models.DateTimeField(auto_now_add=True)
    bloqueado = models.BooleanField(default=True, editable=False, help_text="Garantiza inmutabilidad ISO 17025")

    class Meta:
        verbose_name = "Cálculo de Incertidumbre"
        verbose_name_plural = "Cálculos de Incertidumbre"

    def save(self, *args, **kwargs):
        # Auto-calcular Incertidumbre Expandida: U = uc * k
        if self.incertidumbre_combinada and self.presupuesto_utilizado:
            self.incertidumbre_expandida = float(self.incertidumbre_combinada) * float(
                self.presupuesto_utilizado.factor_cobertura)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"U para {self.registro_tecnico.folio_registro}: ±{self.incertidumbre_expandida} {self.unidades}"