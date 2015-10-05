# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth import (
	login as login_to_site,
	logout as logout_from_site,
	update_session_auth_hash as update_session
)
from django.shortcuts import render_to_response, redirect, RequestContext
from django.contrib.auth.tokens import default_token_generator as tokens
from django.utils.http import urlsafe_base64_decode as base64_decode
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from apps.fmfn.forms import LoginForm, RecoveryForm
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.http import HttpResponseForbidden
from django.utils.http import force_text
from apps.fmfn.models import ActionLog
from django.views.generic import View

__all__ = [
	'login',
	'logout',
	'recover'
]
User = get_user_model()

class LoginView(View):

	def get(self, request):

		# Check if user has been authenticated before - if so, redirect him/her to the main site
		if request.user is not None and request.user.is_authenticated():

			ActionLog.objects.log_account('User redirected since already logged in', user = request.user, status = 302)
			return redirect(reverse_lazy('index'))

		# Create the login form and render the template
		form = LoginForm()
		return render_to_response('accounts/login.html', context = RequestContext(request, locals()))
	@method_decorator(csrf_protect)
	def post(self, request):

		# Check if user has been authenticated before - if so, redirect him/her to the main site
		if request.user is not None and request.user.is_authenticated():

			ActionLog.objects.log_account('User redirected since already logged in', user = request.user, status = 302)
			return redirect(reverse_lazy('index'))

		form = LoginForm(request.POST)
		if form.is_valid():

			# Login the authenticated user to the site and redirect - remember to log this event
			user = form.user
			ActionLog.objects.log_account('User logged in to site (current permissions: %s)' % user.groups, user = user, status = 200)
			login_to_site(request, user)

			return redirect(reverse_lazy('index'))

		# Login failed - report errors back to the user
		ActionLog.objects.log_account('Failed attempt to log in to site (requested account: %s)' % form.cleaned_data['email_address'], status = 401)

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
		ActionLog.objects.log_account('User logged out from site', user = user)

		# Proceed to log out the user
		logout_from_site(request)
		return redirect(reverse_lazy('accounts:login'))

logout = LogoutView.as_view()

class RecoverView(View):

	def get(self, request, user_id = '', token = '', stage = ''):

		# Check if user has been authenticated before - if so, redirect him/her to the main site
		if request.user is not None and request.user.is_authenticated():

			ActionLog.objects.log_account('User redirected since already logged in', user = request.user, status = 302)
			return redirect(reverse_lazy('index'))

		# This view is based on recovery stage. There are two stages: "recover" and "reset".
			# In "recover", the user account is identified and a next steps mail is sent to the user's email address
			# In "reset", the user is prompted to set a new password
		# The GET method processes both stages' form rendering. Care is taken to make this as legible as possible, and
		# as commented as possible
		if stage == 'recover':

			# We are in "recover" stage: we must ask the user for the account he/she wishes to recover
			# Add the recovery form, in "recover" mode, and render the stuff
			form = RecoveryForm(stage = stage)
			return render_to_response('accounts/recover.html', context = RequestContext(request, locals()))

		elif stage == 'reset':

			# We are in "reset" stage: we must validate the token and, if valid, prompt the user to reset his/her password
			# Identify the user - if the user is invalid, we may have an in-progress security breach
			try: user = User.objects.get(id = int(force_text(base64_decode(user_id))))
			except User.DoesNotExist: user = None

			if user is None or not tokens.check_token(user, token):

				# The URL has been tampered with - abort right now
				ActionLog.objects.log_account('URL tampering attempt detected: aborting recovery process', status = 403, user = user)
				return HttpResponseForbidden()

			form = RecoveryForm(stage = stage, user = user)
			return render_to_response('accounts/reset.html', context = RequestContext(request, locals()))

		return HttpResponseForbidden()
	@method_decorator(csrf_protect)
	def post(self, request, user_id = '', token = '', stage = ''):

		# Check if user has been authenticated before - if so, redirect him/her to the main site
		if request.user is not None and request.user.is_authenticated():

			ActionLog.objects.log_account('User redirected since already logged in', user = request.user, status = 302)
			return redirect(reverse_lazy('index'))

		if stage == 'recover':

			# Create the form in "recover" mode and attempt to validate it
			form = RecoveryForm(request.POST, stage = stage)
			if form.is_valid():

				# The form was submitted correctly, thus we send the email and notify the user on further steps
				user = form.user
				ActionLog.objects.log_account('Initiated account recovery for user (current permissions: %s)' % user.groups, user = user, status = 200)
				form.send_recovery_email(request, user, tokens.make_token(user))

				return render_to_response('accounts/recovering.html', context = RequestContext(request, locals()))

			# The account is invalid: notify this error to the user and log it
			email = form.cleaned_data['email_address']
			ActionLog.objects.log_account('Attempted to recover password of invalid account (email address: %s)' % email, status = 401)

			return render_to_response('accounts/recover.html',
				context = RequestContext(request, locals()),
				status = 401
			)
		elif stage == 'reset':

			# Identify the user - if the user is invalid, we may have an in-progress security breach
			try: user = User.objects.get(id = int(force_text(base64_decode(user_id))))
			except User.DoesNotExist: user = None

			if user is None or not tokens.check_token(user, token):

				# The URL has been tampered with - abort right now
				ActionLog.objects.log_account('URL tampering attempt detected: aborting recovery process', status = 403, user = user)
				return HttpResponseForbidden()

			# Validate the user data using the form in "complete" mode
			form = RecoveryForm(request.POST, stage = stage, user = user)
			if form.is_valid():

				# Reset the user password
				ActionLog.objects.log_account('Resetting password for user account', status = 200, user = user)
				password = form.cleaned_data['password']
				user.set_password(password)
				user.save()

				# Invalidate all sessions since they are no longer valid
				update_session(request, user)
				return redirect(reverse_lazy('accounts:login'), context = RequestContext(request, locals()))

			# The form could not be validated due to incompatible passwords
			ActionLog.objects.log_account('Attempted to change password for user', status = 401, user = user)
			return render_to_response('accounts/reset.html',
				context = RequestContext(request, locals()),
				status = 401
			)

		return HttpResponseForbidden()

recover = RecoverView.as_view()
