# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from apps.fmfn.decorators import role_required, ajax_required
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.http import HttpResponseForbidden
from django.views.generic import View
from django.http import JsonResponse

__all__ = [ 'manage' ]

class PortfolioView(View):

	@method_decorator(login_required)
	@method_decorator(role_required('teacher'))
	def get(self, request, user_id = 0): pass
	@method_decorator(ajax_required)
	@method_decorator(login_required)
	@method_decorator(csrf_protect)
	@method_decorator(role_required('teacher'))
	def put(self, request, user_id = 0, content_id = 0): pass
	@method_decorator(ajax_required)
	@method_decorator(login_required)
	@method_decorator(csrf_protect)
	@method_decorator(role_required('teacher'))
	def delete(self, request, user_id = 0, content_id = 0): pass

manage = PortfolioView.as_view()
