# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from _base import Settings
from os.path import join

class Development(Settings):

	SECRET_KEY = 't5_o87@$2#7ca8==8n=lb67y_2o4zgwv3bp*+k*b*4nfe#k8x2'

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
		'default': { 'BACKEND': 'django.core.cache.backends.locmem.LocMemCache' }
	}

	EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

	LOGGING = {
		'version': 1,
		'disable_existing_loggers': True
	}

	STATIC_ROOT = join(Settings.BASE_DIR, 'static')
	MEDIA_ROOT = join(Settings.BASE_DIR, 'media')
