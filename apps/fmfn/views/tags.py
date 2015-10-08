# -*- coding: utf-8 -*-
from __future__ import unicode_literals
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
from django.http import JsonResponse
from django.views.generic import View
from apps.fmfn.decorators import role_required
from apps.fmfn.models import (
	Type,
	Theme,
	Language,
	ActionLog
)

class TagsView(View):

	@method_decorator(login_required)
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
		if request.is_ajax():
			tags = []
			response_dict = {'type': None, 'data': []}
			type = request.GET['type']

			if type == 'theme':
				response_dict['type'] = 'theme'
				data = Theme.objects.filter(active=True)
			elif type == 'type':
				response_dict['type'] = 'type'
				data = Type.objects.filter(active=True)
			elif type == 'language':
				response_dict['type'] = 'language'
				data = Language.objects.filter(active=True)

			for tag in data:
				tags.append({'id': tag.id, 'name': tag.name})

			response_dict['data'] = tags

			response = JsonResponse(response_dict)

			return response

	def put(self, request):pass

	def post(self, request): pass

	def delete(self, request): pass