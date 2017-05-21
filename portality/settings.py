#-*- coding: utf-8 -*-
"""
Django settings for portality project.

Generated by 'django-admin startproject' using Django 1.8.17.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import json
from collections import namedtuple

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
if (os.environ.has_key('DJANGO_DEBUG')):
    if (os.environ['DJANGO_DEBUG'] == 'Debug'):
        DEBUG = True

ALLOWED_HOSTS = ['gencode.me', 'localhost',]


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
#    'django.contrib.sites',
    'giza',
    'issue',
    'rest_framework',
#    'allauth',
#    'allauth.account',
#    'allauth.socialaccount',
#    'allauth.socialaccount.providers.naver',
)
#SITE_ID = 1

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'portality.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates'),],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'issue.context_processors.global_settings',
#                'django.template.context_processors.request',
            ],
            'debug': DEBUG,
        },
    },
]

WSGI_APPLICATION = 'portality.wsgi.application'

try:
    with open(os.path.join(BASE_DIR, "secrets.json")) as f:
        data = json.loads(f.read())
    SecretsNamedTuple = namedtuple('SecretsNamedTuple', data.keys(), verbose=False)
    secrets = SecretsNamedTuple(*[data[x] for x in data.keys()])
    SECRET_KEY = getattr(secrets, "SECRET_KEY")
    DB_NAME = getattr(secrets, "DB_NAME")
    DB_USER = getattr(secrets, "DB_USER")
    DB_PASSWORD = getattr(secrets, "DB_PASSWORD")
    EMAIL_HOST = getattr(secrets, "EMAIL_HOST")
    EMAIL_HOST_USER = getattr(secrets, "EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = getattr(secrets, "EMAIL_HOST_PASSWORD")
    DEFAUL_FROM_EMAIL = getattr(secrets, "DEFAUL_FROM_EMAIL")
    SERVER_EMAIL = getattr(secrets, "SERVER_EMAIL")
except IOError:
    SECRET_KEY = 'k8n13h0y@$=v$uxg*^brlv9$#hm8w7nye6km!shc*&bkgkcd*p' # test key
    DB_NAME = ''
    DB_USER = ''
    DB_PASSWORD = ''
    EMAIL_HOST_USER = ''
    EMAIL_HOST_PASSWORD = ''
    DEFAUL_FROM_EMAIL = ''
    SERVER_EMAIL = ''

EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases
DATABASES = {
    'default': {
         'ENGINE': 'django.db.backends.postgresql_psycopg2',
         'NAME': DB_NAME,
         'USER': DB_USER,
         'PASSWORD': DB_PASSWORD,
         'HOST': 'localhost',
         'PORT': '',
    }
}

REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
#    'allauth.account.auth_backends.AuthenticationBackend'
)


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Seoul'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/assets/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
)

MEDIA_URL = '/upload/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'upload')

LOGIN_REDIRECT_URL = 'login'

# Setting for issue
FILTER_DATE_DELTA = 7 # 핫이슈에 개제될 시간(일)
HOTISSUE_LIMIT = 20 # 핫이슈 리스트 개수
MEDIA_CHOICE = ( # 매체 종류
         ('조선일보', '조선일보'),
         ('중앙일보', '중앙일보'),
         ('동아일보', '동아일보'),
         ('한겨레', '한겨레'),
         ('경향신문', '경향신문'),
         ('오마이뉴스', '오마이뉴스'),
         ('미디어오늘', '미디어오늘'),
         ('KBS', 'KBS'),
         ('MBC', 'MBC'),
         ('SBS', 'SBS'),
         ('TV조선', 'TV조선'),
         ('채널A', '채널A'),
         ('JTBC', 'JTBC'),
         ('MBN', 'MBN'),
         ('YTN', 'YTN'),
         ('연합뉴스', '연합뉴스'),
         ('뉴시스', '뉴시스'),
         ('뉴스1', '뉴스1'),
         ('국민일보', '국민일보'),
         ('노컷뉴스', '노컷뉴스'),
         ('뉴데일리', '뉴데일리'),
         ('뉴스타파', '뉴스타파'),
         ('뉴스토마토', '뉴스토마토'),
         ('뉴스핌', '뉴스핌'),
         ('데일리안', '데일리안'),
         ('매일경제', '매일경제'),
         ('머니투데이', '머니투데이'),
         ('문화일보', '문화일보'),
         ('민중의소리', '민중의소리'),
         ('서울신문', '서울신문'),
         ('세계일보', '세계일보'),
         ('시사iN', '시사iN'),
         ('시사저널', '시사저널'),
         ('위키트리', '위키트리'),
         ('이데일리', '이데일리'),
         ('쿠키뉴스', '쿠키뉴스'),
         ('프레시안', '프레시안'),
         ('한국경제', '한국경제'),
         ('한국일보', '한국일보'),
    )
GIZA_IMAGE_SIZE_LIMIT = 100 * 1024 # 기자 사진 사이즈 제한
