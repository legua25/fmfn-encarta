# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from configurations.values import *
from _base import Settings
from os.path import join

class Production(Settings):

	SECRET_KEY = SecretValue(environ_name = 'SECRET')

	DEBUG = False
	ALLOWED_HOSTS = [  # TODO: Set this up on the server
		'localhost'
	]
	ADMINS = []  # TODO: Set this up on the server
	MANAGERS = ADMINS
	DISALLOWED_USER_AGENTS = []  # TODO: Set this up on the server

	DATABASES = {
		'default': {
			'ENGINE': 'django.db.backends.mysql',
			'HOST': 'localhost',
			'NAME': SecretValue(environ_name = 'DATABASE_NAME'),
			'USER': SecretValue(environ_name = 'DATABASE_USER'),
			'PASSWORD': SecretValue(environ_name = 'DATABASE_PASSWD')
		}
	}

	CACHES = {
		'default': {
			'BACKEND': 'django_pylibmc.memcached.PyLibMCCache',
			'TIMEOUT': 500,
			'BINARY': True,
			'OPTIONS': { 'tcp_nodelay': True }
		}
	}

	EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
	EMAIL_HOST = ''  # TODO: Set this up on the server
	EMAIL_PORT = ''  # TODO: Set this up on the server
	EMAIL_HOST_USER = SecretValue(environ_name = 'MAILING_USER')
	EMAIL_HOST_PASSWORD = SecretValue(environ_name = 'MAILING_PASSWD')

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

	STATIC_ROOT = ''  # TODO: Set this up on the server
