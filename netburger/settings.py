from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = 'replace-me-in-production'
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'cardapio',
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

ROOT_URLCONF = 'netburger.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'netburger.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = []

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Sessão do carrinho
CART_SESSION_ID = 'carrinho'

# Autenticação
LOGIN_URL = 'admin_login'
LOGIN_REDIRECT_URL = 'admin_painel'
LOGOUT_REDIRECT_URL = 'menu_cardapio'

# Ajuste de timezone para Brasil, se preferir usar 'America/Sao_Paulo' altere abaixo
TIME_ZONE = 'America/Sao_Paulo'

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
TEMPLATE_DIRS = [BASE_DIR / 'templates']

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Numero do WhatsApp da loja usado para gerar o link do pedido
WHATSAPP_NUMERO_LOJA = os.environ.get('WHATSAPP_NUMERO_LOJA', '5565993481587')
