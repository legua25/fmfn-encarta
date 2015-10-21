# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from apps.fmfn.decorators import role_required, ajax_required
from apps.fmfn.models import ActionLog, Material, Portfolio
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.http import HttpResponseForbidden
from django.views.generic import View
from django.http import JsonResponse

__all__ = [ 'manage' ]

class PortfolioView(View):

	@method_decorator(login_required)
	@method_decorator(role_required('teacher'))
	def get(self, request, user_id = 0): pass
	@method_decorator(ajax_required)
	@method_decorator(login_required)
	@method_decorator(csrf_protect)
	@method_decorator(role_required('teacher'))
	def put(self, request, content_id = 0):

		# Get the material by ID
		try: material = Material.objects.get(id = content_id)
		except Material.DoesNotExist:

			ActionLog.objects.log_content('Failed to retrieve material \'%s\'' % content_id, status = 401, user = request.user)
			return HttpResponseForbidden()
		else:

			# Verify the material was not already added
			portfolio = Portfolio.objects.user(request.user)
			if portfolio.materials.filter(id = content_id).exists():

				ActionLog.objects.log_content('Attempted to add already included material \'%s\'' % content_id, status = 401, user = request.user)
				return HttpResponseForbidden()

			# Save the material
			portfolio.materials.add(material)
			ActionLog.objects.log_content('User added material \'%s\' to portfolio' % content_id, status = 201, user = request.user)

			# Serialize material and return response
			try: material_content = material.content.url
			except ValueError: material_content = ''

			return JsonResponse({
				'version': '1.0.0',
				'status': 201,
				'material': {
					'id': content_id,
					'title': material.title,
					'description': material.description,
					'content': material_content,
					'link': material.link
				}
			}, status = 201)
	@method_decorator(ajax_required)
	@method_decorator(login_required)
	@method_decorator(csrf_protect)
	@method_decorator(role_required('teacher'))
	def delete(self, request, content_id = 0): pass

manage = PortfolioView.as_view()
