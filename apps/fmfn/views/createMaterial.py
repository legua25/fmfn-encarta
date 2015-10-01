# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import redirect, render_to_response, RequestContext
from django.contrib.auth import login as login_to_site
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse_lazy
from django.views.generic import View
from apps.fmfn.forms import materials

__all__ = [ 'createMaterial' ]


class CreateMaterialView(View):

	def post(self,request):

		# Validate the form
		form = materials(request.POST)
		if form.is_valid():

			# Log in the user into the system
			title = form.title
			description = form.description

			# Redirect the user to the main site
			return redirect(reverse_lazy('home'))

		return render_to_response('accounts/login.html', context = RequestContext(request, locals()), status = 401)
login = CreateMaterialView.as_view()
