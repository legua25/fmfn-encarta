# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import redirect, render_to_response, RequestContext
from django.contrib.auth import login as login_to_site
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse_lazy
from django.views.generic import View
from apps.fmfn.forms import LoginForm

__all__ = [ 'login' ]

class LoginView(View):

	def get(self, request):

		# If the user is already logged in, redirect him/her to the main site
		if request.user is not None and request.user.is_authenticated(): return redirect(reverse_lazy('home'))

		form = LoginForm()
		return render_to_response('accounts/login.html', context = RequestContext(request, locals()))

	@method_decorator(csrf_protect)
	def post(self, request):

		# If the user is already logged in, redirect him/her to the main site
		if request.user is not None and request.user.is_authenticated(): return redirect(reverse_lazy('home'))

		# Validate the form
		form = LoginForm(request.POST)
		if form.is_valid():

			# Log in the user into the system
			user = form.user
			login_to_site(request, user)

			# Redirect the user to the main site
			return redirect(reverse_lazy('home'))

		return render_to_response('accounts/login.html', context = RequestContext(request, locals()), status = 401)

login = LoginView.as_view()
