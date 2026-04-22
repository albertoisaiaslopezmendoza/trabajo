import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'django-insecure-0+w@3v8wtwm$h^dx!o65y-u73!ny5-yxi+e$aa6x5pcsy+dx#-'
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'm00_imparcialidad',
    'm01_limpieza',
    'm02_documentos',
    'm03_revision_contrato',
    'm04_manual',
    'm05_control_documental',
    'm06_riesgos_oportunidades',
    'm07_acciones_correctivas',
    'a00_auditoria',
    'a03_mapa_procesos',
    'a04_mapa_procesos',
    'aa_m01_revision_contrato',
    'a_m07_roles_permisos',
    'm11_reactivos',
    'b_m02_clientes',
    'b_m17_gestion_quejas',
    'c_m03_muestreo',
    'c_m04_recepcion',
    'd_m08_equipos',
    'd_m09_trazabilidad',
    'e_m05_metodos_sops',
    'e_m06_competencia_personal',
    'e_m07_condiciones_ambientales',
    'e_m12_ejecucion_registros',
    'e_m13_calculos_incertidumbre',
    'e_m14_aseguramiento_validez',
    'crispy_forms',
    'crispy_bootstrap5',
    'module',
    'login',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'main_one.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'main_one.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# --- CAMBIOS DE IDIOMA Y ZONA HORARIA ---
LANGUAGE_CODE = 'es-mx'  # Cambiado de 'en-us' a Español México
TIME_ZONE = 'America/Mexico_City' # Cambiado de 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = 'static/'
LOGIN_URL = '/login/'
LOGIN_REDIRECT_URL = '/'

# --- CONFIGURACIÓN PARA GUARDAR ARCHIVOS (PDFs) ---
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Configuración de Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"