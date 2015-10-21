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

	@method_decorator(login_required)
	@method_decorator(ajax_required)
	@method_decorator(role_required('content manager'))
	def get(self, request, tag_type = ''):

		# Retrieve parameters
		filters = request.GET.get('filter', '')

		# Query all tags from the specified tag, if valid
		if tag_type == 'theme': data = Theme.objects.active().filter(name__icontains = filters)
		elif tag_type == 'type': data = Type.objects.active().filter(name__icontains = filters)
		elif tag_type == 'language': data = Language.objects.active().filter(name__icontains = filters)
		else:

			# If type is invalid, return error
			ActionLog.objects.log_tags('Failed to display %s tags' % tag_type, user = request.user, status = 401)
			return HttpResponseForbidden()

		# Return tags list JSON
		ActionLog.objects.log_tags('Displayed %s tags' % tag_type, user = request.user, status = 200)
		return JsonResponse({
			'version': '1.0.0',
			'status': 200,
			'type': tag_type,
			'data': [ { 'id': tag.id, 'name': tag.name } for tag in data ]
		})
	@method_decorator(login_required)
	@method_decorator(ajax_required)
	@method_decorator(role_required('content manager'))
	def post(self, request, tag_id = 0, tag_type = '', action = ''):

		# Tag creation request
		if action == 'create':

			# Retrieve parameters
			name = request.POST['name']

			# Determine tag type, if valid
			if tag_type == 'type': tag_cls = Type
			elif tag_type == 'theme': tag_cls = Theme
			elif tag_type == 'language': tag_cls = Language
			else:
				# If not valid, return error
				ActionLog.objects.log_tags('Failed to create tag entry (id: %s)' % tag_id, user = request.user, status = 401)
				return HttpResponseForbidden()

			# Ensure that a tag with the same name does not exist
			if bool(tag_cls.objects.filter(name__iexact = name)) is False:

				# Create tag
				tag = tag_cls.objects.create(name = name)

				# Return response JSON
				ActionLog.objects.log_tags('Created tag entry (id: %s)' % tag_id, user = request.user, status = 201)
				return JsonResponse({
					'version': '1.0.0',
					'status': 201,
					'data': { 'type': tag_type, 'id': tag.id, 'name': tag.name }
				}, status = 201)

			# Return duplicate tag response JSON
			ActionLog.objects.log_tags('Failed to create tag entry (id: %s)' % tag_id, user = request.user, status = 302)
			return JsonResponse({
				'version': '1.0.0',
				'status': 302
			}, status = 302)

		# Tag edition request
		elif action == 'edit':

			# Retrieve tag name
			name = request.POST['name']

			# Determine tag type and update tag name
			if tag_type == 'theme': tag_cls = Theme
			elif tag_type == 'type': tag_cls = Type
			elif tag_type == 'language': tag_cls = Language
			else: return HttpResponseForbidden()

			tag_cls.objects.filter(id = tag_id).update(name = name)
			ActionLog.objects.log_tags('Edited tag entry (id: %s)' % tag_id, user = request.user, status = 201)

			# Return response JSON
			return JsonResponse({
				'version': '1.0.0',
				'status': 200,
				'data': { 'type': tag_type, 'id': tag_id, 'name': name }
			})
	@method_decorator(login_required)
	@method_decorator(ajax_required)
	@method_decorator(role_required('content manager'))
	def delete(self, request, tag_type = '', tag_id = 0, action = ''):

		# Determine tag type and delete specified tag, if valid
		if tag_type == 'theme': Theme.objects.get(id = tag_id).delete()
		elif tag_type == 'type': Type.objects.get(id = tag_id).delete()
		elif tag_type == 'language': Language.objects.get(id = tag_id).delete()
		else:
			# If not valid, return an error
			ActionLog.objects.log_tags('Failed to delete tag entry (id: %s)' % tag_id, user = request.user, status = 401)
			return HttpResponseForbidden()

		# Return response JSON
		ActionLog.objects.log_tags('Deleted tag entry (id: %s)' % tag_id, user = request.user, status = 200)
		return JsonResponse({
			'version': '1.0.0',
			'status': 200
		})

tags = TagsView.as_view()