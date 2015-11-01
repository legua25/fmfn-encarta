# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from apps.fmfn.models import (
	Material,
	Type,
	Theme,
	Language
)
from django.shortcuts import render_to_response, redirect, RequestContext
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from apps.fmfn.decorators import role_required, ajax_required
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.db.models import Q

class ListMaterialView(View):

	@method_decorator(login_required)
	@method_decorator(role_required('parent'))
	def get(self, request, content_id = 0):

		paginator = Paginator(Material.objects.active(), request.GET.get('page_size', 25))
		page = request.GET.get('page', 1)

		try: materials = paginator.page(page)
		except EmptyPage: materials = paginator.page(paginator.num_pages)
		except PageNotAnInteger: materials = paginator.page(1)

		return render_to_response('materials/list.html', context = RequestContext(request, locals()))

class FilterMaterialView(View):

	@method_decorator(login_required)
	@method_decorator(ajax_required)
	@method_decorator(role_required('parent'))
	def get(self, request, content_id = 0):

		# Retrieve parameters
		filters = request.GET.get('filter', '')

		data = Material.objects.get(
			Q(name__icontains = filters) |
			Q(title__icontains = filters) |
			Q(description__icontains = filters) |
		    Q(language__name__icontains = filters)
		)

		# Return tags list JSON
		ActionLog.objects.log_content('Located tag cluster', user = request.user)
		return JsonResponse({
			'version': '1.0.0',
			'status': 200,
			'data': [ { 'id': m.id, 'title': m.title, 'description': m.description } for m in data ]
		})


