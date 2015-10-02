# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import (
	login as login_to_site,
	logout as logout_from_site,
	authenticate
)
from django.shortcuts import render_to_response, redirect, RequestContext
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse_lazy
from apps.fmfn.models import ActionLog
from apps.fmfn.forms import LoginForm
from django.views.generic import View

__all__ = [
	'login',
	'logout'
]

class LoginView(View):

	def get(self, request):

		# Check if user has been authenticated before - if so, redirect him/her to the main site
		if request.user is not None and request.user.is_authenticated():

			ActionLog.objects.create(
				user = request.user,
				action = 'User redirected since already logged in',
				status = 302,
				category = 1
			)
			return redirect(reverse_lazy('index'))

		# Create the login form and render the template
		form = LoginForm()
		return render_to_response('accounts/login.html', context = RequestContext(request, locals()))
	def post(self, request):

		# Check if user has been authenticated before - if so, redirect him/her to the main site
		if request.user is not None and request.user.is_authenticated():

			ActionLog.objects.create(
				user = request.user,
				action = 'User redirected since already logged in',
				status = 302,
				category = 1
			)
			return redirect(reverse_lazy('index'))

		form = LoginForm(request.POST)
		if form.is_valid():

			# Login the authenticated user to the site and redirect - remember to log this event
			user = form.user
			ActionLog.objects.create(
				user = user,
				action = 'User logged in to site (current permissions: %s)' % user.groups,
				status = 200,
				category = 1
			)
			login_to_site(request, user)

			return redirect(reverse_lazy('index'))

		# Login failed - report errors back to the user
		ActionLog.objects.create(
			action = 'Failed attempt to log in to site (requested account: %s)' % form.cleaned_data['email_address'],
			category = 1,
			status = 401
		)

		return render_to_response('accounts/login.html',
			context = RequestContext(request, locals()),
			status = 401
		)

login = LoginView.as_view()

class LogoutView(View):

	@method_decorator(login_required)
	def get(self, request):

		# User is logging out - log this event
		user = request.user
		ActionLog.objects.create(
			user = user,
			action = 'User logged out from site',
			category = 1,
			status = 200
		)

		# Proceed to log out the user
		logout_from_site(request)
		return redirect(reverse_lazy('accounts:login'))

logout = LogoutView.as_view()
