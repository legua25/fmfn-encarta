# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from apps.fmfn.models import ActionLog, Material, Portfolio, Item
from django.shortcuts import render_to_response, RequestContext
from apps.fmfn.decorators import role_required, ajax_required
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
	def get(self, request):

		portfolio = Portfolio.objects.user(request.user)

		paginator = Paginator(portfolio.items.filter(active = True), request.GET.get('page_size', 15))
		page = request.GET.get('page', 1)

		try: items = paginator.page(page)
		except EmptyPage: items = paginator.page(paginator.num_pages)
		except PageNotAnInteger: items = paginator.page(1)

		return render_to_response('materials/portfolio.html', context = RequestContext(request, locals()))
	@method_decorator(ajax_required)
	@method_decorator(login_required)
	@method_decorator(csrf_protect)
	@method_decorator(role_required('teacher'))
	def put(self, request, content_id = 0):

		# Attempt to load the material
		try: material = Material.objects.active().get(id = content_id)
		except Material.DoesNotExist:

			ActionLog.objects.log_content('Failed to locate material with ID \'%s\'' % content_id, status = 403, user = request.user)
			return HttpResponseForbidden()
		else:

			# Check the material is not already added
			portfolio = Portfolio.objects.user(request.user)
			if portfolio.items.filter(material = material, active = True).exists():

				ActionLog.objects.log_content('Cannot add already added material', status = 403, user = request.user)
				return HttpResponseForbidden()

			# Add the item to the portfolio
			portfolio.items.create(material = material, portfolio = portfolio)
			ActionLog.objects.log_content('Added material ID \'%s\' to user portfolio' % content_id, status = 201, user = request.user)

			# Serialize the material
			return JsonResponse({
				'version': '1.0.0',
				'status': 201,
				'material': {
					'id': material.id,
					'title': material.title,
					'description': material.description,
					'content': material.content.url if bool(material.content) is True else None,
					'link': material.link
				}
			}, status = 201)
	@method_decorator(ajax_required)
	@method_decorator(login_required)
	@method_decorator(csrf_protect)
	@method_decorator(role_required('teacher'))
	def delete(self, request, content_id = 0):

		# Attempt to load the material
		try: material = Material.objects.active().get(id = content_id)
		except Material.DoesNotExist:

			ActionLog.objects.log_content('Failed to locate material with ID \'%s\'' % content_id, status = 403, user = request.user)
			return HttpResponseForbidden()
		else:

			# Check the material is not already added
			portfolio = Portfolio.objects.user(request.user)
			if not portfolio.items.filter(active = True).filter(material = material).exists():

				ActionLog.objects.log_content('Cannot remove non-included material', status = 403, user = request.user)
				return HttpResponseForbidden()

			# Add the item to the portfolio
			portfolio.items.filter(active = True).get(material = material).delete()
			ActionLog.objects.log_content('Removed material ID \'%s\' to user portfolio' % content_id, user = request.user)

			# Serialize the material
			return JsonResponse({
				'version': '1.0.0',
				'status': 200,
				'material': {
					'id': material.id,
					'title': material.title
				}
			})

manage = PortfolioView.as_view()
