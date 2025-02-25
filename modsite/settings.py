import os
from pathlib import Path
import cloudinary  # Correto
import cloudinary.uploader
import cloudinary.api


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))




# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-3@f!7%ad6(07yk67&ossrgantu@l)g#7lv-b3oo%qzlj8q6v7r'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['127.0.0.1', 'kr-mods-d517b12a9a57.herokuapp.com', 'krsoftwares.com.br']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mods',  # Adicionando nosso app mods
    'cloudinary_storage',
    'cloudinary',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'modsite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'mods.context_processors.get_logo',  # Adicionamos o Context Processor
                'mods.context_processors.redes_sociais',  # Adicionando nosso contexto
            ],
        },
    },
]

WSGI_APPLICATION = 'modsite.wsgi.application'



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),  # Corrigido para evitar o erro
    }
}

import dj_database_url  

DATABASES['default'] = dj_database_url.config(
    conn_max_age=600,
    conn_health_checks=True,
)


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


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Configuração de arquivos estáticos (já deve estar no seu código)
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Configuração de mídia
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')




DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = "/login/"



SESSION_ENGINE = "django.contrib.sessions.backends.db"
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 3600  # Sessão dura 1 hora
# Configuração para envio de e-mails (Gmail)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'jnsvirtual1311@gmail.com'  # Substitua pelo seu e-mail
EMAIL_HOST_PASSWORD = 'kpyp lwss rlkr ejqg'  # Substitua pela senha do seu e-mail

cloudinary.config( 
    cloud_name = "dvd7rkwyu", 
    api_key = "416561564897632", 
    api_secret = "xOlGgthqR_2IqdhFnnI54WtJYt8", # Click 'View API Keys' above to copy your API secret
    secure=True
)

DEFAULT_FILE_STORAGE  =  'cloudinary_storage.storage.MediaCloudinaryStorage'