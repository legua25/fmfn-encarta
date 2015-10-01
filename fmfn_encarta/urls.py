# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.views.generic.base import RedirectView
from django.core.urlresolvers import reverse_lazy
from django.conf.urls import include, url
from django.contrib import admin

from apps.fmfn import views

urlpatterns = [

	url(r'^', include([

		# Index (redirects to login view if applicable)
		url(r'^$', RedirectView.as_view(url = reverse_lazy('login'), permanent = True), name = 'index'),

		# Main site
		url(r'^site/', include([ url(r'^$', views.home, name = 'home') ])),

		# Account control
		url(r'^accounts/', include([

			url(r'^login/$', views.login, name = 'login')
			# TODO: Add more URLs

		]))

	])),

	url(r'^admin/', include(admin.site.urls))

]
