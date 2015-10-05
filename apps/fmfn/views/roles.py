# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render_to_response, redirect, RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.contrib.auth.models import Group as Role
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from apps.fmfn.models import ActionLog
from django.views.generic import View
from apps.fmfn.forms import RoleForm

__all__ = [ 'roles' ]
User = get_user_model()

class RoleView(View):

	@method_decorator(login_required)
	def put(self, request, user_id = 0, role_id = 0): pass
	@method_decorator(login_required)
	def delete(self, request, user_id = 0, role_id = 0): pass

roles = RoleView.as_view()
