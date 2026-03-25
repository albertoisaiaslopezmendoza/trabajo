# a00_auditoria/models.py
from django.db import models
from django.utils import timezone

class AuditLog(models.Model):
    created_at = models.DateTimeField(default=timezone.now, verbose_name="Fecha / hora")
    user_id = models.BigIntegerField(null=True, blank=True)
    username = models.CharField(max_length=255, null=True, blank=True, verbose_name="Usuario")
    module = models.CharField(max_length=100, null=True, blank=True, verbose_name="Módulo")
    action = models.CharField(max_length=100, null=True, blank=True, verbose_name="Acción")
    details = models.TextField(null=True, blank=True, verbose_name="Detalle")
    ip_address = models.CharField(max_length=50, null=True, blank=True)
    hostname = models.CharField(max_length=255, null=True, blank=True)
    app_name = models.CharField(max_length=100, null=True, blank=True)
    level = models.CharField(max_length=20, null=True, blank=True)
    ok = models.BooleanField(null=True, blank=True)
    meta = models.JSONField(default=dict, blank=True)

    class Meta:
        db_table = 'audit_log'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.created_at.strftime('%Y-%m-%d %H:%M:%S')} - {self.action} by {self.username}"