"""
Django settings for webapps project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import ConfigParser

config = ConfigParser.ConfigParser()
config.read("config.ini")

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'c^&4nu_&u=(_)-l&%mw*of^&l)i5t7z+2z==*-f^_rhx)+4^^n'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'socialnetwork'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'webapps.urls'

WSGI_APPLICATION = 'webapps.wsgi.application'

LOGIN_URL = "/login"

LOGIN_REDIRECT_URL = "/frontPage"
# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.environ.get('DB-NAME'),
        'USER': os.environ.get('DB-USER'),
        'PASSWORD': os.environ.get('DB-PASSWORD'),
        'HOST': os.environ.get('DB-HOST'),
        'PORT': os.environ.get('DB-PORT')
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'EST'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'


## Handle emailing from webapp

# Prints email out to terminal
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


## Enables REAL emails to be sent from email specific in config.ini
# EMAIL_HOST = config.get('Email', 'Host')
# EMAIL_PORT = config.get('Email', 'Port')
# EMAIL_HOST_USER = config.get('Email', 'User')
# EMAIL_HOST_PASSWORD = config.get('Email', 'Password')
# EMAIL_USE_SSL = True
# print 'EMAIL_HOST',EMAIL_HOST+':'+str(EMAIL_PORT)
# print 'EMAIL_HOST_USER',EMAIL_HOST_USER
