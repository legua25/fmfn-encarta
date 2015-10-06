# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView
from django.conf.urls import include, url
from django.contrib import admin
from apps.fmfn import views

redirect = RedirectView.as_view

urlpatterns = [

	# Search interface
	url(r'^', include([

		url(r'^$', redirect(reverse_lazy('search')), name = 'index'),  # GET
		url(r'^search/$', include([
			url(r'^$', None, name = 'search'),  # GET
			url(r'^api/$', None, name = 'filter')  # POST
		]))

	])),
	# Content management
	url(r'^content/', include([

		url(r'create/$', None, name = 'create'),  # GET, PUT
		url(r'^(?P<content_id>[\d]+)/', include([

			url(r'^$', None, name = 'view'),  # GET
			url(r'^edit/$', None, name = 'edit')  # GET, POST, DELETE

		])),
		
		url(r'^$', views.list_material, name = 'list'),  # GET
		
		url(r'^tags/', include([

			url(r'^$', None, name = 'list'),  # GET
			url(r'^create/$', None, name = 'create'),  # PUT
			url(r'^(?P<tag_id>[\d]+)/edit/$', None, name = 'edit')  # POST, DELETE

		], namespace = 'content-tags', app_name = 'fmfn'))

	], namespace = 'content', app_name = 'fmfn')),
	# Account management
	url(r'^accounts/', include([

		url(r'^login/$', None, name = 'login'),  # GET, POST
		url(r'^logout/$', None, name = 'logout'),  # GET
		url(r'^recover/', include([

			url(r'^request/$', None, name = 'recover'),  # GET, PUT
			url(r'^complete/$', None, name = 'complete')  # GET, PATCH

		]))

	], namespace = 'accounts', app_name = 'fmfn')),
	# User management
	url(r'^users/', include([

		url(r'^$', None, name = 'list'),  # GET
		url(r'^api/$', None, name = 'filter'),  # POST
		url(r'^(?P<user_id>[\d]+)/', include([

			url(r'^$', None, name = 'view'),  # GET
			url(r'^edit/$', None, name = 'edit'),  # GET, POST, DELETE
			url(r'^portfolio/$', None, name = 'portfolio')  # GET, PUT, DELETE

		]))

	], namespace = 'users', app_name = 'fmfn')),
	# Management
	url(r'^manage/', include([

		url(r'^statistics/', None, name = 'stats'),  # GET
		url(r'^reports/', include([

			url(r'^$', None, name = 'list'),  # GET
			url(r'^create/$', None, name = 'create'),  # PUT
			url(R'^(?P<report_id>[\d]+)/$', None, name = 'manage')  # PATCH

		])),
		url(r'^log/$', None, name = 'logging'),
		url(r'^advanced/', include(admin.site.urls))

	], namespace = 'management', app_name = 'fmfn'))

]
