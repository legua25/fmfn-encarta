# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse_lazy
from django.views.generic import RedirectView
from django.conf.urls import include, url
from django.contrib import admin
from apps.fmfn import views

from django.http import HttpResponse
from django.template import Template, Context

redirect = RedirectView.as_view

urlpatterns = [

	# Search interface
	url(r'^', include([

		url(r'^$', redirect(url = reverse_lazy('search')), name = 'index'),  # GET
		url(r'^search/$', include([

			url(r'^$', views.search.search, name = 'search'),  # GET
	 		url(r'^api/$', views.search.search, name = 'filter')  # POST

		]))

	])),

	# Content management
	 url(r'^content/', include([

	 	url(r'create/$', views.materials.create, name = 'create'),  # GET, PUT
	 	url(r'^(?P<content_id>[\d]+)/', include([

	 		url(r'^$',views.materials.view, name = 'view'),  # GET, #POST
	 		url(r'^edit/$', views.materials.edit, name = 'edit')  # GET, POST, DELETE

	 	]))

	 ], namespace = 'content', app_name = 'apps.fmfn')),

	# Tags
	url(r'^tags/(?P<tag_type>type|theme|language)/', include([

        url(r'^$', views.tags.tags, name = 'list'),  # GET
        url(r'^create/$', views.tags.tags, name = 'create', kwargs = { 'action': 'create' }),  # POST
        url(r'^(?P<tag_id>[\d]+)/edit/$', views.tags.tags, name = 'edit', kwargs = { 'action': 'edit' })  # POST, DELETE

    ], namespace = 'tags', app_name = 'fmfn')),

	# Account management
	url(r'^accounts/', include([

		url(r'^login/$', views.accounts.login, name = 'login'),  # GET, POST
		url(r'^logout/$', views.accounts.logout, name = 'logout'),  # GET
		url(r'^recover/', include([

			url(r'^$', views.accounts.recover, name = 'recover', kwargs = { 'stage': 'recover' }),  # GET, POST
			url(r'^reset/(?P<user_id>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.accounts.recover, name = 'reset', kwargs = { 'stage': 'reset' })  # GET, POST

		]))

	], namespace = 'accounts', app_name = 'apps.fmfn')),
	
	# User management
	url(r'^users/', include([

	# 	url(r'^$', None, name = 'list'),  # GET
	# 	url(r'^api/$', None, name = 'filter'),  # POST
		url(r'^create/$', views.users.create, name = 'create'),  # GET, POST
	 	url(r'^(?P<user_id>[\d]+)/', include([

	 		url(r'^$',  lambda request, user_id = 0: HttpResponse(''), name = 'view'),  # GET, POST
	 		url(r'^edit/$', views.users.edit, name = 'edit')  # GET, POST, DELETE

		]))

	], namespace = 'users', app_name = 'apps.fmfn')),

	# Portfolio (favorites) management
	url(r'^portfolio/', include([

		url(r'^$', views.portfolio.manage, name = 'view'),  # GET
		url(r'^(?P<content_id>[\d]+)/$', views.portfolio.manage, name = 'edit')  # PUT, DELETE

	], namespace = 'portfolio', app_name = 'fmfn')),

	# Management
	# url(r'^manage/', include([

	# 	url(r'^statistics/', None, name = 'stats'),  # GET
	# 	url(r'^reports/', include([

	# 		url(r'^$', None, name = 'list'),  # GET
	# 		url(r'^create/$', None, name = 'create'),  # PUT
	# 		url(R'^(?P<report_id>[\d]+)/$', None, name = 'manage')  # PATCH

	# 	])),
	# 	url(r'^log/$', None, name = 'logging'),
	# 	url(r'^advanced/', include(admin.site.urls))

	# ], namespace = 'management', app_name = 'apps.fmfn'))

]