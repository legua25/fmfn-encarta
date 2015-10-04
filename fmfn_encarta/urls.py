# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView
from django.conf.urls import include, url
from django.contrib import admin
from apps.fmfn import views

from django.http import HttpResponse

redirect = RedirectView.as_view

urlpatterns = [

	# Search interface
	url(r'^', include([

		url(r'^$', redirect(url = reverse_lazy('search')), name = 'index'),  # GET
		url(r'^search/$', include([
			# TODO: Remove this lambda - it's useless and does nothing
			url(r'^$', lambda request: HttpResponse(''), name = 'search'),  # GET
	#  		url(r'^api/$', None, name = 'filter')  # POST
		]))

	])),
	# Content management
	# url(r'^content/', include([
	#
	# 	url(r'create/$', None, name = 'create'),  # GET, PUT
	# 	url(r'^(?P<content_id>[\d]+)/', include([
	#
	# 		url(r'^$', None, name = 'view'),  # GET
	# 		url(r'^edit/$', None, name = 'edit')  # GET, POST, DELETE
	#
	# 	])),
	# 	url(r'^tags/', include([
	#
	# 		url(r'^$', None, name = 'list'),  # GET
	# 		url(r'^create/$', None, name = 'create'),  # PUT
	# 		url(r'^edit/$', None, name = 'edit')  # POST, DELETE
	#
	# 	], namespace = 'content-tags', app_name = 'fmfn'))
	#
	# ], namespace = 'content', app_name = 'apps.fmfn')),
	# Account management
	url(r'^accounts/', include([

		url(r'^login/$', views.login, name = 'login'),  # GET, POST
		url(r'^logout/$', views.logout, name = 'logout'),  # GET
		url(r'^recover/', include([

			url(r'^$', views.recover, name = 'recover', kwargs = { 'stage': 'request' }),  # GET, POST
			url(r'^complete/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.recover,
			    name = 'complete',
			    kwargs = { 'stage': 'complete' }
			)  # GET, PATCH

		]))

	], namespace = 'accounts', app_name = 'apps.fmfn')),
	# User management
	# url(r'^users/', include([
	#
	# 	url(r'^$', None, name = 'list'),  # GET
	# 	url(r'^api/$', None, name = 'filter'),  # POST
	# 	url(r'^(?P<user_id>[\d]+)/', include([
	#
	# 		url(r'^$', None, name = 'view'),  # GET
	# 		url(r'^edit/$', None, name = 'edit'),  # GET, POST, DELETE
	# 		url(r'^portfolio/$', None, name = 'portfolio')  # GET, PUT, DELETE
	#
	# 	]))
	#
	# ], namespace = 'users', app_name = 'apps.fmfn')),
	# Management
	# url(r'^manage/', include([
	#
	# 	url(r'^statistics/', None, name = 'stats'),  # GET
	# 	url(r'^reports/', include([
	#
	# 		url(r'^$', None, name = 'list'),  # GET
	# 		url(r'^create/$', None, name = 'create'),  # PUT
	# 		url(R'^(?P<report_id>[\d]+)/$', None, name = 'manage')  # PATCH
	#
	# 	])),
	# 	url(r'^log/$', None, name = 'logging'),
	# 	url(r'^advanced/', include(admin.site.urls))
	#
	# ], namespace = 'management', app_name = 'apps.fmfn'))

]
