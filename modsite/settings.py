import os
from pathlib import Path
import dj_database_url
import cloudinary
import cloudinary.uploader
import cloudinary.api
from dotenv import load_dotenv
load_dotenv()

EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")


# Diretório base do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Segurança
SECRET_KEY = os.getenv('SECRET_KEY', 'chave-secreta-de-desenvolvimento')
DEBUG = os.getenv('DEBUG', 'False') == 'True'

ALLOWED_HOSTS = ['127.0.0.1', 'kr-mods-d517b12a9a57.herokuapp.com', 'krsoftwares.com.br']

# Aplicações instaladas
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'mods',  # Seu app principal
    'cloudinary_storage',  # Armazenamento de mídia no Cloudinary
    'cloudinary',  # Biblioteca Cloudinary
]

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Para servir arquivos estáticos no Heroku
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# Configuração do Django Templates
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
                'mods.context_processors.get_logo',  # Context Processor customizado
                'mods.context_processors.redes_sociais',  # Outro contexto customizado
            ],
        },
    },
]

WSGI_APPLICATION = 'modsite.wsgi.application'

# Banco de Dados - Padrão Heroku PostgreSQL
DATABASES = {
    'default': dj_database_url.config(conn_max_age=600, conn_health_checks=True)
}

# Validações de senha
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internacionalização
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Configuração de arquivos estáticos no Heroku
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Configuração de armazenamento no Cloudinary
cloudinary.config(
    cloud_name=os.getenv('CLOUDINARY_CLOUD_NAME', 'dvd7rkwyu'),
    api_key=os.getenv('CLOUDINARY_API_KEY', '416561564897632'),
    api_secret=os.getenv('CLOUDINARY_API_SECRET', 'xOlGgthqR_2IqdhFnnI54WtJYt8'),
    secure=True
)

# Armazenamento de arquivos de mídia no Cloudinary
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
MEDIA_URL = '/media/'  # Mantemos para referência, mas não é necessário para Cloudinary

# Configuração de login e sessão
LOGIN_REDIRECT_URL = '/'
LOGOUT_REDIRECT_URL = '/'
LOGIN_URL = "/login/"
SESSION_ENGINE = "django.contrib.sessions.backends.db"
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 3600  # Sessão expira após 1 hora

# Configuração de email (Gmail)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'jnsvirtual1311@gmail.com'
EMAIL_HOST_PASSWORD = 'kpyp lwss rlkr ejqg'  # 🚨 **Não exponha credenciais no código! Use variáveis de ambiente**

# Configuração padrão para novos modelos do Django
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
