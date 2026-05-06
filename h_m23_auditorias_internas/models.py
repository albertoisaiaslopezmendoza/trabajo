# h_m23_auditorias_internas/models.py
from django.db import models
from django.contrib.auth.models import User  # Asumiendo que usas el User de Django


class InternalAudit(models.Model):
    STATUS_CHOICES = [
        ('PLANNED', 'Planeada'),
        ('DONE', 'Realizada'),
        ('CLOSED', 'Cerrada'),
    ]

    audit_code = models.CharField("Código de Auditoría", max_length=50, unique=True)
    planned_date = models.DateField("Fecha Planeada", null=True, blank=True)
    performed_date = models.DateField("Fecha Realizada", null=True, blank=True)
    scope = models.TextField("Alcance", blank=True)
    lead_auditor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                     verbose_name="Auditor Líder")
    status = models.CharField("Estatus", max_length=20, choices=STATUS_CHOICES, default='PLANNED')

    # report_attachment = models.FileField(upload_to='audits/', null=True, blank=True) # Opcional para adjuntos

    def __str__(self):
        return f"{self.audit_code} - {self.get_status_display()}"


class AuditFinding(models.Model):
    FINDING_TYPES = [
        ('NC', 'No Conformidad'),
        ('OBS', 'Observación'),
        ('OPPORTUNITY', 'Oportunidad de Mejora'),
    ]

    SEVERITY_CHOICES = [
        ('BAJA', 'Baja'),
        ('MEDIA', 'Media'),
        ('ALTA', 'Alta'),
        ('CRITICA', 'Crítica'),
    ]

    audit = models.ForeignKey(InternalAudit, on_delete=models.CASCADE, related_name='findings',
                              verbose_name="Auditoría")
    finding_type = models.CharField("Tipo de Hallazgo", max_length=20, choices=FINDING_TYPES)
    description = models.TextField("Descripción del Hallazgo")
    severity = models.CharField("Severidad", max_length=20, choices=SEVERITY_CHOICES, null=True, blank=True)
    related_process = models.CharField("Proceso Relacionado", max_length=100, blank=True)

    def __str__(self):
        return f"{self.finding_type} - {self.audit.audit_code}"