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
from apps.fmfn.forms import UserCreationForm, UserEditForm, AdminUserEditForm, UserVisualizationForm

__all__ = [ 'create', 'edit' , 'view']
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

		ActionLog.objects.log_debug('EditUser:GET', status = 200, user = request.user)
		user_target = User.objects.get(id = user_id)

		# Is the user role an admin?
		if request.user.belongs_to('user manager'):
			form = AdminUserEditForm(instance = user_target)
			return render_to_response('users/edit.html', context = RequestContext(request, locals()))
		else:
			# Is an non admin user role trying to edit someone else?
			if user_target.id != request.user.role_id:
				ActionLog.objects.log_users('Attempted to view/edit other user account without enough privileges', status = 401, user = request.user)
				return HttpResponseForbidden('Forbidden Get Operation Requested')

			# Display a bounded form with the user details
			else:
				form = UserEditForm(instance = user_target)
				return render_to_response('users/patch.html', context = RequestContext(request, locals()))


	@method_decorator(login_required)
	@method_decorator(csrf_protect)
	@method_decorator(role_required('user manager'))
	def post(self, request, user_id = 0):

		#Redirect petition to its correct predefined behavior:
		if request.POST.get('_method', 'post'):
			ActionLog.objects.log_debug('EditUser:POST', status = 200, user = request.user)
		elif request.POST.get('_method', 'patch'):
			ActionLog.objects.log_debug('EditUser:patch', status = 200, user = request.user)
			return self.patch(request, user_id)
		elif request.POST.get('_method', 'delete'):
			ActionLog.objects.log_debug('EditUser:delete', status = 200, user = request.user)
			return self.delete(request, user_id)
		else:
			return HttpResponseForbidden()

		#Post default behaviour
		form = AdminUserEditForm(request.POST, request.FILES, instance = User.objects.get(id = user_id))
		if form.is_valid():

			form.instance.save()
			return redirect(reverse_lazy('users:view', kwargs = { 'user_id': user_id }))

		# form is not valid, show form errors:
		ActionLog.objects.log_users('Invalid form submitted at user post', status = 401, user = request.user)
		return render_to_response('users/edit.html',
			context = RequestContext(request, locals()),
		    status = 401
		)

	@method_decorator(login_required)
	@method_decorator(csrf_protect)
	def patch(self, request, user_id = 0):
		ActionLog.objects.log_debug('EditUser:PATCH', status = 200, user = request.user)

		if request.user.id != user_id:
			ActionLog.objects.log_users('Attempted to patch other account', status = 401, user = request.user)
			return HttpResponseForbidden('Forbidden Patch Operation Requested')

		form = UserEditForm(request.POST, request.FILES, instance = User.objects.get(id = user_id))

		if form.is_valid():
			ActionLog.objects.log_users('User %s account modified' % user_id, status = 200, user = request.user)
			form.instance.save()
			return redirect(reverse_lazy('users:view', kwargs = { 'user_id': user_id }))

		# form is not valid, show form errors:
		ActionLog.objects.log_users('Invalid form submitted at user patch', status = 401, user = request.user)
		return render_to_response('users/edit.html',
			context = RequestContext(request, locals()),
		    status = 401
		)

	@method_decorator(login_required)
	@method_decorator(role_required('user manager'))
	def delete(self, request, user_id = 0):
		ActionLog.objects.log_debug('EditUser:delete', status = 200, user = request.user)

		# User shouldn't be able to delete their own account
		if user_id == request.user.id:

			ActionLog.objects.log_account('Attempted to erase own account', status = 401, user = request.user)
			return HttpResponseForbidden()

		User.objects.active().filter(id = user_id).update(active = False)

		ActionLog.objects.log_account('Deleted user "%s"' % user_id, user = request.user)
		return redirect(reverse_lazy('index'), context = RequestContext(request, locals()))


edit = EditUserView.as_view()

class ConsultUserView(View):

	@method_decorator(login_required)
	def get(self, request, user_id = 0):
		user_target = User.objects.get(id = user_id)
		form = UserVisualizationForm(instance = user_target)
		return render_to_response('users/view.html', context = RequestContext(request, locals()))

	@method_decorator(login_required)
	def post(self, request, user_id = 0):
		# Redirect to user list
			return redirect(reverse_lazy('index'), context = RequestContext(request, locals()))
view = ConsultUserView.as_view()