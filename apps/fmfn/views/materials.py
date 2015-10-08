# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import redirect, render_to_response, RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as login_to_site
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse_lazy
from apps.fmfn.models import Material, ActionLog
from apps.fmfn.forms import MaterialForm
from apps.fmfn.decorators import role_required
from django.views.generic import View

__all__ = [ 'create', 'edit' ]

class CreateMaterialView(View):

	#@method_decorator(login_required)
	#@method_decorator(role_required('content manager'))
	def get(self, request):

		form = MaterialForm()
		return render_to_response('materials/create.html', context = RequestContext(request, locals()))
	@method_decorator(login_required)
	@method_decorator(role_required('content manager'))
	def post(self, request):

		form = MaterialForm(request.POST)
		if form.is_valid():

			# TODO: Adjust material creation - use ModelForm instead
			material = form.instance
			material.user = request.user
			material.save()

			ActionLog.objects.log_content('Material "%s" created' % material.title, status = 201, user = request.user)
			return redirect(reverse_lazy('index'))

		ActionLog.objects.log_content('Failed to create material, validation error.', status = 401)
		return render_to_response('materials/create.html',
			context = RequestContext(request, locals()),
			status = 401
		)
		# TODO: Redirect user to form (again) and present errors

create = CreateMaterialView.as_view()

class EditMaterialView(View):

	@method_decorator(login_required)
	@method_decorator(role_required('content manager'))
	def get(self, request, content_id = 0):

		ActionLog.objects.log_content('Requested material "%s"' % content_id, status = 200, user = request.user)

		form = MaterialForm(request.POST, instance = Material.objects.active().get(id = content_id))
		return render_to_response('materials/create.html', context = RequestContext(request, locals()))
	@method_decorator(login_required)
	@method_decorator(role_required('content manager'))
	def post(self, request, content_id = 0):

		form = MaterialForm(request.POST, instance = Material.objects.active().get(id = content_id))

		if form.is_valid():

			material = form.instance
			material.save()

			ActionLog.objects.log_content('Edited material "%s"' % content_id, status = 200, user = request.user)
			return redirect(reverse_lazy('content:view', kwargs = { 'content_id': content_id }))

		ActionLog.objects.log_content('Failed to edit material "%s"' % content_id, status = 401, user = request.user)
		return render_to_response('materials/create.html', context = RequestContext(request, locals()))
	@method_decorator(login_required)
	@method_decorator(role_required('content manager'))
	def delete(self, request, content_id = 0):

		Material.objects.active().filter(id = content_id).update(active = False)

		ActionLog.objects.log_content('Deleted material "%s"' % content_id, status = 200, user = request.user)
		return redirect(reverse_lazy('search'))

edit = EditMaterialView.as_view()
