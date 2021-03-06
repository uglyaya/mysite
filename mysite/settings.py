# coding:utf-8
"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 1.8.16.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os,sys
from django.conf.global_settings import MEDIA_URL
from mysite import settings_local

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

reload(sys)
sys.setdefaultencoding('utf-8')
gettext = lambda s: s
# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'z$3wp6zflifn%hs4^ohrk!c7ep-qx#9zri(*lorl&e+gzif7(+'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

LANGUAGES = (
    ('en', gettext('English')),
    ('zh-hans', gettext('Chinese')),
)

# Application definition

INSTALLED_APPS = ( 
#     'suit',
#     'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'hooked_server', 
    'smart_selects', 
    'xadmin',
    'crispy_forms',
    'reversion', 
)
#https://github.com/digi604/django-smart-selects
# JQUERY_URL = True
USE_DJANGO_JQUERY = False


MIDDLEWARE_CLASSES = (
 #   'django.middleware.gzip.GZipMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.locale.LocaleMiddleware', #1、语言更改 第一次登录的时候显示的是英文，要改成中文，只需在MIDDLEWARE_CLASSES添加 django.middleware.locale.LocaleMiddleware，并确保它在’django.contrib.sessions.middleware.SessionMiddleware’之后 即可。
)

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.i18n', #多语言需要加的模版
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


XADMIN_CONF = 'web.xsite'
WSGI_APPLICATION = 'mysite.wsgi.application'


# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'Asia/Shanghai'
USE_TZ = False
USE_I18N = True 
USE_L10N = True
 
 
try:
    from settings_local import *
except ImportError:
    pass
