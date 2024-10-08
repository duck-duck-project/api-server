import contextlib
from pathlib import Path

import cloudinary.api
from environ import Env

BASE_DIR = Path(__file__).resolve().parent.parent

env = Env()
env.read_env(BASE_DIR / '.env')

SECRET_KEY = env.str('SECRET_KEY')

DEBUG = env.bool('DEBUG')

ALLOWED_HOSTS = env.list('ALLOWED_HOSTS')

TELEGRAM_BOT_TOKEN = env.str('TELEGRAM_BOT_TOKEN')

CORS_ALLOWED_ORIGINS = env.list('CORS_ALLOWED_ORIGINS')

ENABLE_IN_DEBUG_FOR_UNHANDLED_EXCEPTIONS = env.bool(
    'ENABLE_IN_DEBUG_FOR_UNHANDLED_EXCEPTIONS',
    default=False,
)

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_celery_beat',
    'rest_framework',
    'corsheaders',
    'import_export',
    'drf_standardized_errors',
    'users',
    'secret_messages',
    'economics',
    'food_menu',
    'holidays',
    'quizzes',
    'mining',
    'user_characteristics',
    'relationships',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'duck_duck.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            BASE_DIR / "templates",
        ]
        ,
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

WSGI_APPLICATION = 'duck_duck.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env.str('DATABASE_NAME'),
        'USER': env.str('DATABASE_USER'),
        'HOST': env.str('DATABASE_HOST'),
        'PORT': env.str('DATABASE_PORT'),
        'PASSWORD': env.str('DATABASE_PASSWORD'),
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation'
                '.NumericPasswordValidator',
    },
]

DRF_STANDARDIZED_ERRORS = {
    'ENABLE_IN_DEBUG_FOR_UNHANDLED_EXCEPTIONS': (
        ENABLE_IN_DEBUG_FOR_UNHANDLED_EXCEPTIONS
    ),
}

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'
STATIC_ROOT = BASE_DIR / 'static'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    ),
    "EXCEPTION_HANDLER": "drf_standardized_errors.handler.exception_handler"
}
DRF_STANDARDIZED_ERRORS = {
    "EXCEPTION_FORMATTER_CLASS": "core.exceptions.CustomFormatter",
}

cloudinary.config(
    cloud_name=env.str('CLOUDINARY_CLOUD_NAME'),
    api_key=env.str('CLOUDINARY_API_KEY'),
    api_secret=env.str('CLOUDINARY_API_SECRET'),
)

if DEBUG:
    INSTALLED_APPS.append('silk')
    MIDDLEWARE.append('silk.middleware.SilkyMiddleware')
