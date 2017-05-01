import os

from django.utils.translation import ugettext_lazy as _

from . import local_settings as ls

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ls.SECRET_KEY

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = ls.DEBUG

ALLOWED_HOSTS = ls.ALLOWED_HOSTS


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rosetta',
    # 'debug_toolbar',
    'paypal.standard.ipn',
    'haystack',
    'apps.shop',
    'apps.cart',
    'apps.orders',
    'apps.accounts',
    'apps.coupons',
    'apps.payment',
]

MIDDLEWARE = [
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = '_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.i18n',
                'apps.shop.context_processors.menu_categories',
                'apps.cart.context_processors.cart',
            ],
        },
    },
]

WSGI_APPLICATION = '_project.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': ls.DB_NAME,
        'USER': ls.DB_USER,
        'PASSWORD': ls.DB_PASSWORD,
        'HOST': ls.DB_HOST,
        'PORT': ls.DB_PORT
    }
}


# Cache
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}


# Fulltext search
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.'
                  'ElasticsearchSearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'products',
    },
}

HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.'
             'UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.'
             'MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.'
             'CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.'
             'NumericPasswordValidator', },
]


# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'uk_UA'
TIME_ZONE = 'Europe/Kiev'
USE_I18N = True
USE_L10N = True
USE_TZ = True

LOCALE_PATHS = (os.path.join(BASE_DIR, 'locale'), )
LANGUAGES = (
    # ('en', _('English')),
    ('uk_UA', _('Ukrainian')),
)

ROSETTA_STORAGE_CLASS = 'rosetta.storage.CacheRosettaStorage'

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static"), ]
STATIC_ROOT = os.path.join(BASE_DIR, '..', 'static/')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'media')

CART_SESSION_ID = 'cart'

PAYPAL_RECEIVER_EMAIL = ls.PAYPAL_RECEIVER_EMAIL
PAYPAL_TEST = ls.PAYPAL_TEST

ADMIN_MAIL = ls.ADMIN_MAIL

MAILCHIMP_API_KEY = ls.MAILCHIMP_API_KEY
MAILCHIMP_USERNAME = ls.MAILCHIMP_USERNAME
MAILCHIMP_LIST_ID = ls.MAILCHIMP_LIST_ID

# Email
# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

if DEBUG:
    EMAIL_HOST = '127.0.0.1'
    EMAIL_HOST_USER = ''
    EMAIL_HOST_PASSWORD = ''
    EMAIL_PORT = 1025
    EMAIL_USE_TLS = False

INTERNAL_IPS = '127.0.0.1'
