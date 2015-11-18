# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from configurations.values import *
from _base import Settings
from os.path import join

class Production(Settings):

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
			'NAME': 'fmfn',
			'USER': 'fmfn_user',
			'PASSWORD': 'VHSBLnRquEFyPAbZ'
		}
	}

	CACHES = {
		'default': {
			'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
			'TIMEOUT': 500,
			'BINARY': True,
			'OPTIONS': { 'tcp_nodelay': True }
		}
	}

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

	# Enable Security Settings
	SECURE_BROWSER_XSS_FILTER = True
	SECURE_CONTENT_TYPE_NOSNIFF = True
	X_FRAME_OPTIONS = 'DENY'
	CSRF_COOKIE_HTTPONLY = True
	
	# Static and media directory configurations
	MEDIA_ROOT = '/var/www/media/'
	MEDIA_URL = '/media/'
	STATIC_ROOT = '/var/www/static/'
	STATIC_URL = '/static/'
