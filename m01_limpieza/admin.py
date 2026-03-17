from django.contrib import admin
from .models import ActivoLimpieza, RegistroLimpieza

@admin.register(ActivoLimpieza)
class ActivoAdmin(admin.ModelAdmin):
    list_display = ('codigo_barras', 'nombre', 'area', 'frecuencia_dias', 'activo')
    search_fields = ('nombre', 'codigo_barras')

@admin.register(RegistroLimpieza)
class RegistroAdmin(admin.ModelAdmin):
    list_display = ('fecha_hora', 'nombre_activo_snapshot', 'realizado_por', 'estado', 'proximo_vencimiento')
    list_filter = ('estado', 'tipo_limpieza')
    readonly_fields = ('uuid', 'fecha_hora', 'evidencia_pdf')