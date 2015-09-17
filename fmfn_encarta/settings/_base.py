# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from os.path import dirname, abspath, join
from configurations import Configuration

class Settings(Configuration):

	BASE_DIR = dirname(dirname(dirname(abspath(__file__))))
	SECRET_KEY = ''

	DEBUG = True
	ALLOWED_HOSTS = []

	ROOT_URLCONF = 'fmfn_encarta.urls'
	WSGI_APPLICATION = 'fmfn_encarta.wsgi.application'

	INSTALLED_APPS = [

		'grappelli',
		'autocomplete_light',
		'django.contrib.sites',
		'django.contrib.admin',
		'django.contrib.auth',
		'django.contrib.contenttypes',
		'django.contrib.sessions',
		'django.contrib.messages',
		'django.contrib.staticfiles',
	    'haystack',
		'dbmail',
		'imagekit',
		'widget_tweaks',

	]
	MIDDLEWARE_CLASSES = [

		'django.contrib.sessions.middleware.SessionMiddleware',
		'django.middleware.common.CommonMiddleware',
		'django.middleware.csrf.CsrfViewMiddleware',
		'django.contrib.auth.middleware.AuthenticationMiddleware',
		'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
		'django.contrib.messages.middleware.MessageMiddleware',
		'django.middleware.clickjacking.XFrameOptionsMiddleware',
		'django.middleware.security.SecurityMiddleware',
		'django_downloadview.SmartDownloadMiddleware'

	]

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
				],
			},
		}
	]

	CSRF_COOKIE_AGE = 1800

	EMAIL_SUBJECT_PREFIX = '[FMFN] '

	LANGUAGE_CODE = 'en-us'
	TIME_ZONE = 'America/Mexico_City'
	USE_I18N = True
	USE_L10N = True
	USE_TZ = True

	LANGUAGES = [
		('en-us', _('English (United States)')),
		('es-mx', _('Spanish (Mexico)'))
	]

	STATIC_URL = '/static/'
	MEDIA_URL = '/media/'
	MEDIA_ROOT = join(BASE_DIR, 'media')

	SESSION_COOKIE_AGE = 1800

	HAYSTACK_CONNECTIONS = {
		'default': {
			'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
			'PATH': join(BASE_DIR, 'whoosh_index'),
			'STORAGE': 'file',
			'POST_LIMIT': 128 * 1024 * 1024,
			'INCLUDE_SPELLING': True,
			'BATCH_SIZE': 100
		}
	}
	DOWNLOADVIEW_BACKEND = 'django_downloadview.nginx.XAccelRedirectMiddleware'
	DOWNLOADVIEW_RULES = []
