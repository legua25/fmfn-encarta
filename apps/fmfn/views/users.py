# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render_to_response, redirect, RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse_lazy
from apps.fmfn.decorators import role_required
from django.contrib.auth import get_user_model
from apps.fmfn.models import ActionLog, users
from django.http import HttpResponseForbidden
from django.views.generic import View
from apps.fmfn.forms import UserCreationForm, UserEditForm, AdminUserEditForm

__all__ = [ 'create', 'edit' ]
User = get_user_model()

class CreateUserView(View):

	@method_decorator(login_required)
	@method_decorator(role_required('user manager'))
	def get(self, request):

		form = UserCreationForm()
		return render_to_response('users/create.html', context = RequestContext(request, locals()))
	@method_decorator(login_required)
	@method_decorator(role_required('user manager'))
	def post(self, request):

		# Create and validate the form
		form = UserCreationForm(request.POST)
		if form.is_valid():

			# Retrieve the user, set the password, and create him/her
			user, password = form.instance, form.cleaned_data['password']
			user.set_password(password)
			user.save()

			# Redirect to user list
			return redirect(reverse_lazy('users:list'))

		return render_to_response('users/create.html',
			context = RequestContext(request, locals()),
		    status = 401
		)

create = CreateUserView.as_view()

class EditUserView(View):

	@method_decorator(login_required)
	def get(self, request, user_id = 0):
		user_target = User.objects.get(id = user_id)
		if request.user.role_id == 3 or request.user.role_id == 4:
			form = AdminUserEditForm(request.POST, instance = user_target)
			return render_to_response('users/edit.html', context = RequestContext(request, locals()))
		else:
			# Is an non admin user role trying to edit someone else?
			if user_target.id != request.user.role_id:
				ActionLog.objects.log_account('Attempted to view/edit other user account without enough privileges', status = 401, user = request.user)
				return HttpResponseForbidden('Forbidden Get Operation Requested')
			else:
				form = UserEditForm(request.POST, instance = user_target)
				return render_to_response('users/patch.html', context = RequestContext(request, locals()))


	@method_decorator(login_required)
	@method_decorator(csrf_protect)
	@method_decorator(role_required('user manager'))
	def post(self, request, user_id = 0):

		form = AdminUserEditForm(request.POST, instance = User.objects.get(id = user_id))

		if form.is_valid():

			form.instance.save()
			return redirect(reverse_lazy('users:view', kwargs = { 'user_id': user_id }))

		return render_to_response('users/edit.html',
			context = RequestContext(request, locals()),
		    status = 401
		)

	@method_decorator(login_required)
	@method_decorator(csrf_protect)
	def patch(self, request, user_id = 0):

		if request.user.id != user_id:
			ActionLog.objects.log_account('Attempted to patch other account', status = 401, user = request.user)
			return HttpResponseForbidden('Forbidden Patch Operation Requested')

		form = UserEditForm(request.POST, instance = User.objects.get(id = user_id))

		if form.is_valid():

			form.instance.save()
			return redirect(reverse_lazy('users:view', kwargs = { 'user_id': user_id }))

		return render_to_response('users/edit.html',
			context = RequestContext(request, locals()),
		    status = 401
		)

	@method_decorator(login_required)
	@method_decorator(role_required('user manager'))
	def delete(self, request, user_id = 0):
		
		if user_id == request.user.id:

			ActionLog.objects.log_account('Attempted to erase own account', status = 401, user = request.user)
			return HttpResponseForbidden()

		User.objects.active().filter(id = user_id).update(active = False)

		ActionLog.objects.log_account('Deleted user "%s"' % user_id, user = request.user)
		return redirect(reverse_lazy('index'), context = RequestContext(request, locals()))


edit = EditUserView.as_view()