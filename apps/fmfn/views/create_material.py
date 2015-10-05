# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import redirect, render_to_response, RequestContext
from django.contrib.auth import login as login_to_site
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse_lazy
from django.views.generic import View
from apps.fmfn.forms import CreateMaterialForm
from django.contrib.auth.decorators import login_required
from apps.fmfn.models import Material

__all__ = [ 'create_material' ]


class CreateMaterialView(View):

	@method_decorator(login_required)
	def post(self,request):
		form = CreateMaterialForm(request.POST)
		if form.is_valid():
			Material.objects.create(form)
			ActionLog.objects.create()
			return redirect(reverse_lazy('index'))

create_material = CreateMaterialView.as_view()