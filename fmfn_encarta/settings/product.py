# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from configurations.values import *
from _base import Settings
from os.path import join

class Production(Settings):

	#SECRET_KEY = SecretValue(environ_name = 'SECRET')
	SECRET_KEY = 'mj-j+vnfbvzdhn8cg5dvj@h9aeu&p$(3c3@%t2+lw7v+uv8a4l'
	DEBUG = False
	ALLOWED_HOSTS = [  # TODO: Set this up on the server
		'*'
		#'localhost',
		#'159.203.251.186'
	]
	ADMINS = []  # TODO: Set this up on the server
	MANAGERS = ADMINS
	DISALLOWED_USER_AGENTS = []  # TODO: Set this up on the server

	DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.mysql',
			'HOST': 'localhost',
			#'NAME': SecretValue(environ_name = 'DATABASE_NAME'),
			'NAME': 'fmfn',
			#'USER': SecretValue(environ_name = 'DATABASE_USER'),
			'USER': 'fmfn_user',
			#'PASSWORD': SecretValue(environ_name = 'DATABASE_PASSWD')
			'PASSWORD': 'VHSBLnRquEFyPAbZ'
		}
	}

	CACHES = {
		'default': {
			#'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
			'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
			'TIMEOUT': 500,
			'BINARY': True,
			'OPTIONS': { 'tcp_nodelay': True }
		}
	}

	#EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
	#EMAIL_HOST = ''  # TODO: Set this up on the server
	#EMAIL_PORT = ''  # TODO: Set this up on the server
	#EMAIL_HOST_USER = SecretValue(environ_name = 'MAILING_USER')
	#EMAIL_HOST_PASSWORD = SecretValue(environ_name = 'MAILING_PASSWD')

	FILE_UPLOAD_MAX_MEMORY_SIZE = 2621440

	LOGGING = {
		'version': 1,
		'disable_existing_loggers': False,
		'handlers': {
			'file': {
				'level': 'DEBUG',
				'class': 'logging.FileHandler',
				'filename': join(Settings.BASE_DIR, '/debug.log'),
			},
		},
		'loggers': {
			'django.request': {
				'handlers': [ 'file' ],
				'level': 'INFO',
				'propagate': True,
			},
		},
	}

	MEDIA_ROOT = '/var/www/media/'
	MEDIA_URL = '/media/'
	STATIC_ROOT = '/var/www/static/'
	STATIC_URL = '/static/'
