"""
Django settings for expresstire project.
"""
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-dev-key-change-me-7x!k#9m2p')

DEBUG = os.environ.get('DJANGO_DEBUG', 'False') == 'True'

ALLOWED_HOSTS = os.environ.get('DJANGO_ALLOWED_HOSTS', '.onrender.com,localhost,127.0.0.1').split(',')

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'tires',
    'orders',
    'bookings',
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

ROOT_URLCONF = 'expresstire.urls'

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
                'tires.context_processors.cart_context',
                'tires.context_processors.shop_info',
                'tires.context_processors.payment_methods',
            ],
        },
    },
]

WSGI_APPLICATION = 'expresstire.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'zh-hant'
TIME_ZONE = 'Asia/Hong_Kong'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

SHOP_NAME = 'ExpressTire'
SHOP_PHONE = '+852 2345 6789'
SHOP_WHATSAPP = '+852 9683 1170'
SHOP_EMAIL = 'info@expresstire.com'
SHOP_ADDRESS = 'G/F, Man Shun Factory Building, 20 Chi Kiang St, To Kwa Wan, KLN'
SHOP_EMERGENCY = '+852 9190 0850'
SHOP_FACEBOOK = 'https://www.facebook.com/WheelHolic'
SHOP_OPENING_HOURS = 'Mon-Sat 8:00am-6:00pm'

PAYMENT_METHODS = [
    ('fps', 'FPS'),
    ('payme', 'PayMe'),
    ('alipay', 'Alipay HK'),
    ('credit_card', 'Credit Card'),
    ('wechat', 'WeChat Pay'),
    ('cash', 'Cash'),
]

CART_SESSION_ID = 'cart'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
