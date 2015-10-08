# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render_to_response, redirect, RequestContext
from django.contrib.auth.tokens import default_token_generator as tokens
from django.utils.http import urlsafe_base64_decode as base64_decode
from apps.fmfn.decorators import role_required, ajax_required
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from apps.fmfn.forms import LoginForm, RecoveryForm
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.http import HttpResponseForbidden
from django.utils.http import force_text
from apps.fmfn.models import ActionLog
from django.http import JsonResponse
from django.views.generic import View
from apps.fmfn.models import (
	Type,
	Theme,
	Language,
	ActionLog
)

__all__ = [ 'tags' ]

class TagsView(View):

	@method_decorator(login_required)
	@method_decorator(ajax_required)
	@method_decorator(role_required('content manager'))
	def get(self, request):
		"""
		Inputs: request.GET['query'] (optional): The filter criteria to use in order to select tags. Defaults to None.
		Outputs:

			A JSON document complying with the following schema:

			{
				"$schema": "http://json-schema.org/draft-04/schema#",

				"id": "http://jsonschema.net/tag-list",
				"type": "object",
				"properties": {

					"type": { "id": "http://jsonschema.net/tag-list/type", "type": "string" },
					"data": {
						"id": "http://jsonschema.net/tag-list/data",
						"type": "array",
						"items": [
							{
								"id": "http://jsonschema.net/tag-list/data/tag",
								"type": "object",
								"properties": {
									"id": { "id": "http://jsonschema.net/tag-list/data/tag/id", "type": "integer" },
									"name": { "id": "http://jsonschema.net/tag-list/data/tag/name", "type": "string" }
								}
							}
						]
					}

				},
				"required": [ "type", "data" ]
			}

			Possible values include:

			{ "type": "theme", "data": [] }
			{ "type": "language", "data": [ { "id": 1, "name": "inglés" } ] }
		"""

		type = request.GET['type']
		filters = request.GET.get('filter', '')

		if type == 'theme': data = Theme.objects.active().filter(name__icontains = filters)
		elif type == 'type': data = Type.objects.active().filter(name__icontains = filters)
		elif type == 'language': data = Language.objects.active().filter(name__icontains = filters)
		else: return HttpResponseForbidden()

		return JsonResponse({
			'version': '1.0.0',
			'status': 200,
			'type': type,
			'data': [ { 'id': tag.id, 'name': tag.name } for tag in data ]
		})
	@method_decorator(login_required)
	@method_decorator(ajax_required)
	@method_decorator(role_required('content manager'))
	def put(self, request):

		type = request.PUT['type']
		name = request.PUT['name']

		if type == 'theme': tag = Theme.objects.create(name = name)
		elif type == 'type': tag = Type.objects.create(name = name)
		elif type == 'language': tag = Language.objects.create(name = name)
		else: return HttpResponseForbidden()

		return JsonResponse({
			'version': '1.0.0',
			'status': 201,
			'data': { 'type': type, 'id': tag.id, 'name': tag.name }
		})
	@method_decorator(login_required)
	@method_decorator(ajax_required)
	@method_decorator(role_required('content manager'))
	def post(self, request, tag_id = 0):

		type = request.POST['type']
		name = request.POST['data']['name']

		if type == 'theme':

			tag = Theme.objects.get(id = tag_id)
			tag.name = name
			tag.save()
		elif type == 'type':

			tag = Theme.objects.get(id = tag_id)
			tag.name = name
			tag.save()
		elif type == 'language':

			tag = Theme.objects.get(id = tag_id)
			tag.name = name
			tag.save()

		return JsonResponse({
			'version': '1.0.0',
			'status': 200,
			'data': { 'type': type, 'id': tag_id, 'name': name }
		})
	@method_decorator(login_required)
	@method_decorator(ajax_required)
	@method_decorator(role_required('content manager'))
	def delete(self, request, tag_id = 0):

		type = request.POST['type']

		if type == 'theme': Theme.objects.filter(id = tag_id).update(active = False)
		elif type == 'type': Theme.objects.filter(id = tag_id).update(active = False)
		elif type == 'language': Theme.objects.filter(id = tag_id).update(active = False)
		else: return HttpResponseForbidden()

		return JsonResponse({
			'version': '1.0.0',
			'status': 200
		})

tags = TagsView.as_view()