# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render_to_response, redirect, RequestContext
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse_lazy
from apps.fmfn.decorators import role_required
from django.contrib.auth import get_user_model
from apps.fmfn.models import ActionLog
from django.views.generic import View
from apps.fmfn.forms import UserCreationForm

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

		return render_to_response('users/create.html', context = RequestContext(request, locals()))

create = CreateUserView.as_view()

class EditUserView(View):

	@method_decorator(login_required)
	def get(self, request, username = '', password = ''):

		form = ProfileForm(request.user)
		return render_to_response('profile_edit.html', context = RequestContext(request, locals()))

	@method_decorator(csrf_protect)
	def user(self, request, username = ''):

		users.objects.filter(username = username).update(**{
			'username': request.POST['username'],
			'email': request.POST['email'],
			'password': request.POST['password']
		})

		return redirect(reverse_lazy('view_profile', kwargs = { 'username': username }))

edit = EditUserView.as_view()