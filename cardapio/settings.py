# netburguer_config/settings.py

import os
from pathlib import Path

# Definição do diretório base
BASE_DIR = Path(__file__).resolve().parent.parent

# ----------------------------------------------------------------------
# 1. Configurações de Aplicativos e Autenticação (Módulo 1)
# ----------------------------------------------------------------------

INSTALLED_APPS = [
    # Apps Padrão do Django
    'django.contrib.admin',
    'django.contrib.auth', # Autenticação
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Nossa Aplicação Principal
    'cardapio', # Nosso app onde estão views, models e urls.
]

# Configuração de redirecionamento de login/logout
# O painel de CRUD/Histórico exige login
LOGIN_URL = 'admin_login'
LOGIN_REDIRECT_URL = 'admin_painel'
LOGOUT_REDIRECT_URL = 'menu_cardapio'


# ----------------------------------------------------------------------
# 2. Configuração de Templates (HTML)
# ----------------------------------------------------------------------

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        # Dizinendo ao Django para procurar templates na pasta 'templates' global
        'DIRS': [os.path.join(BASE_DIR, 'templates')], 
        'APP_DIRS': True, # Também procura templates dentro das pastas de apps
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

# ----------------------------------------------------------------------
# 3. Configuração de Arquivos Estáticos (CSS, Imagens)
# ----------------------------------------------------------------------

# URL base para servir arquivos estáticos no desenvolvimento (ex: /static/style.css)
STATIC_URL = 'static/'

# Caminho onde o Django deve procurar arquivos estáticos
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# ... Outras configurações (DATABASES, LANGUAGE_CODE, TIME_ZONE)