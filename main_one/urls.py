from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from module import views as module_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', module_views.inicio, name='inicio'),
    path('m00/', include('m00_imparcialidad.urls')),
    path('m01/', include('m01_limpieza.urls')),
    path('module/', include('module.urls')),
    path('login/', include('login.urls')),
    path('m02/', include('m02_documentos.urls')),
    path('m03/', include('m03_revision_contrato.urls')),
    path('m04/', include('m04_manual.urls')),
    path('m05/', include('m05_control_documental.urls')),
    path('m06/', include('m06_riesgos_oportunidades.urls')),
    path('m07/', include('m07_acciones_correctivas.urls')),
    path('a00/', include('a00_auditoria.urls')),
    path('a03/', include('a03_mapa_procesos.urls')),
    path('a04/', include('a04_mapa_procesos.urls')),
    path('aa_m01/', include('aa_m01_revision_contrato.urls')),
    path('a_m07/', include('a_m07_roles_permisos.urls')),
    path('m11/', include('m11_reactivos.urls')),
    path('m02-clientes/', include('b_m02_clientes.urls')),
    path('m17-quejas/', include('b_m17_gestion_quejas.urls')),
]

# Esto permite servir los archivos PDF subidos/generados durante el desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)