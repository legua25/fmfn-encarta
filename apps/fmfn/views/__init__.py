# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from accounts import *

from django.views.generic import View

class HomeView(View):

	def get(self, request):

		from django.shortcuts import render_to_response, RequestContext
		return render_to_response('home.html', context = RequestContext(request, locals()))
home = HomeView.as_view()
