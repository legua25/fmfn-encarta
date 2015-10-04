# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import redirect, render_to_response, RequestContext
from django.contrib.auth import login as login_to_site
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.core.urlresolvers import reverse_lazy
from django.views.generic import View
from apps.fmfn.forms import materials

__all__ = [ 'create_material' ]


class CreateMaterialView(View):

	def post(self,request):
		pass
create_material = CreateMaterialView.as_view()