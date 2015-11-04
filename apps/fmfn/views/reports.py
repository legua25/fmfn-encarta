# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import redirect, render_to_response, RequestContext
from apps.fmfn.decorators import role_required, ajax_required
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.http import HttpResponseForbidden
from django.views.generic import View
from django.http import JsonResponse
from apps.fmfn.models import (
	Material,
	Report,
	ActionLog
)

class ReportsView(View):
	"""
		Inputs: request.GET['query'] (optional): The filter criteria to use in order to select tags. Defaults to None.
		Outputs:
​
			A JSON document complying with the following schema:
​
			{
				"$schema": "http://json-schema.org/draft-04/schema#",
​
				"id": "http://jsonschema.net/tag-list",
				"type": "object",
				"properties": {
​
					"data": {
						"id": "http://jsonschema.net/tag-list/data",
						"type": "array",
						"items": [
							{
								"description": "string"
								"material": "object"
								"user": "object"
							}
						]
					}
​
				},
				"required": [ "type", "data" ]
			}
​
			Possible values include:
​
			{ "data": [ { "description": "test", "material": "test_material", "user": "some_user" } ] }
			{ "data": [] }
		"""

	@method_decorator(login_required)
	@method_decorator(role_required('content manager'))
	def get(self, request):
		"""
			Receives a get request and returns a JSON with all active reports currently in progress

		"""

		# Query reports in progress
		reports = Report.objects.active().filter(status = 1)

		# Write action log
		ActionLog.objects.log_reports('Listed reports', user = request.user)

		# Send response
		return render_to_response('reports/view.html', context = RequestContext(request, locals()))

	@method_decorator(login_required)
	@method_decorator(ajax_required)
	@method_decorator(csrf_protect)
	@method_decorator(role_required('teacher'))
	def post(self, request, content_id = 0):
		"""
			Receives a post request and material id, creates new report for that material and returns a JSON response

		"""

		# Attempt to load the material
		try: material = Material.objects.active().get(id = content_id)
		except Material.DoesNotExist:

			# If material doesn't exist, write in action log and returned forbidden response
			ActionLog.objects.log_reports('Failed to locate material with ID \'%s\'' % content_id, status = 403, user = request.user)
			return HttpResponseForbidden()
		else:

			# Get description parameter
			self.description = request.POST['description']

			# Create new report for specified material with the received description. Defaults to "in progress" status
			new_report = Report.objects.create(
				user = request.user,
				material = material,
				description = self.description,
				status = 1
			)

			# Write action log
			ActionLog.objects.log_reports('Created report (id: %s)' % new_report.id, user = request.user, status = 201)

			# Return response JSON
			return JsonResponse({
				'version': '1.0.0',
				'status': 201,
				'data': { 'description': new_report.description, 'material': new_report.material.id, 'user': new_report.user.id }
			}, status = 201)

	@method_decorator(login_required)
	@method_decorator(ajax_required)
	@method_decorator(csrf_protect)
	@method_decorator(role_required('content manager'))
	def patch(self, request, report_id = 0):
		"""
			Receives a patch request and report id. Modifies specified report to "resolved" status and returns JSON

		"""

		# Query database for specified report
		report = Report.objects.get(id = report_id)
		# Change status
		report.status = 2
		report.save()

		# Write action log
		ActionLog.objects.log_reports('Updated report ( id: %s) to resolved' % report_id, user = request.user, status = 201)

		# Return response JSON
		return JsonResponse({
			'version': '1.0.0',
			'status': 200,
			'data': { 'description': report.description, 'material': report.material.id, 'user': report.user.id }
		})

	@method_decorator(login_required)
	@method_decorator(ajax_required)
	@method_decorator(csrf_protect)
	@method_decorator(role_required('content manager'))
	def delete(self, request, report_id = 0):
		"""
			Receives a delete request and report id. Modifies specified report to "rejected" status and returns JSON

		"""

		# Query database for specified report
		report = Report.objects.get(id = report_id)
		# Change status
		report.status = 4
		report.save()

		# Write action log
		ActionLog.objects.log_reports('Rejected report ( id: %s)' % report_id, user = request.user, status = 201)

		# Return response JSON
		return JsonResponse({
			'version': '1.0.0',
			'status': 200,
			'data': { 'description': report.description, 'material': report.material.id, 'user': report.user.id }
		})

reports = ReportsView.as_view()
