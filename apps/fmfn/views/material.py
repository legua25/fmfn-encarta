# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import redirect, render_to_response, RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as login_to_site
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse_lazy
from apps.fmfn.models import Material, ActionLog
from apps.fmfn.forms import CreateMaterialForm
from apps.fmfn.decorators import role_required
from django.views.generic import View

__all__ = [ 'create', 'edit' ]

class CreateMaterialView(View):

	@method_decorator(login_required)
	@method_decorator(role_required('content manager'))
	def get(self, request): pass
	@method_decorator(login_required)
	@method_decorator(role_required('content manager'))
	def post(self,request):

		form = CreateMaterialForm(request.POST)
		if form.is_valid():

			# TODO: Adjust material creation - use ModelForm instead
			material = form
			ActionLog.objects.create()

			return redirect(reverse_lazy('index'))

		# TODO: Redirect user to form (again) and present errors

create = CreateMaterialView.as_view()

class EditMaterialView(View):

	@method_decorator(login_required)
	@method_decorator(role_required('content manager'))
	def get(self,request):
		pass
	@method_decorator(login_required)
	@method_decorator(role_required('content manager'))
	def post(self,request):
		pass
	@method_decorator(login_required)
	@method_decorator(role_required('content manager'))
	def delete(self,request):
		pass

edit = EditMaterialView.as_view()
