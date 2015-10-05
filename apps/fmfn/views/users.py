# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render_to_response, redirect, RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from apps.fmfn.models import ActionLog
from django.views.generic import View

__all__ = [ 'create' ]
User = get_user_model()

class CreateUserView(View):

	@method_decorator(login_required)
	def get(self, request): pass
	@method_decorator(login_required)
	def post(self, request): pass

create = CreateUserView.as_view()
