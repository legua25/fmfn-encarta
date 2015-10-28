# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render_to_response, redirect, RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.views.generic import View

__all__ = [ 'search' ]

class SearchView(View):

	@method_decorator(login_required)
	def get(self, request): return render_to_response('home.html', context = RequestContext(request, locals()))
	@method_decorator(login_required)
	def post(self, request): pass

search = SearchView.as_view()
