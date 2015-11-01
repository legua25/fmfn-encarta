# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from apps.fmfn.models import (
	Material,
	Type,
	Theme,
	Language,
	ActionLog
)
from django.shortcuts import render_to_response, redirect, RequestContext
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from apps.fmfn.decorators import role_required, ajax_required
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.generic import View
from django.db.models import Q, Avg

__all__ = [ 'search' ]

class SearchView(View):

	""" This view handles the material search function. The filters are received and then look in the database
		for materials that match with the filters. The average of the material rating is calculated and added to the
		properties of the object. The number of the materials to be displayed is handle with the paginator method. At
		the end, the objects are returned with a json format.
	"""

	@method_decorator(login_required)
	@method_decorator(role_required('parent'))
	def get(self, request): return render_to_response('home.html', context = RequestContext(request, locals()))
	@method_decorator(login_required)
	@method_decorator(ajax_required)
	@method_decorator(role_required('parent'))
	@method_decorator(cache_page(300))
	def post(self, request):

		# Filter material based on query
		query = Material.objects.active()
		filters = request.POST.get('filter', None)

		if bool(filters) is not False:

			# Preload related elements and perform matching queries against every one of them
			params = Q(title__icontains = filters) | Q(description__icontains = filters)

			for tag_type in [ 'types', 'themes', 'languages' ]:
				params = params | Q(**{'%s__name__icontains' % tag_type: filters })

			query = query.filter(params)

		# Annotate the results with rating average
		query = query.annotate(rating = Avg('comments__rating_value'))

		# Paginate the results and serialize the response
		paginator = Paginator(query, request.GET.get('page_size', 25))
		page = request.GET.get('page', 1)

		try: materials = paginator.page(page)
		except EmptyPage: materials = paginator.page(paginator.num_pages)
		except PageNotAnInteger: materials = paginator.page(1)

		ActionLog.objects.log_content('Queried for materials (filters: %s)' % filters, user = request.user, status = 302)
		return JsonResponse({
			'version': '1.0.0',
			'status': 302,
			'results': [ {
				'id': m.id,
				'title': m.title,
				'description': m.description,
				'rating': int(round(m.rating or 0)),
				'tags': {
					'types': [ t.name for t in m.types.filter(active = True) ],
					'themes': [ t.name for t in m.themes.filter(active = True) ],
					'languages': [ t.name for t in m.languages.filter(active = True) ]
				}
			} for m in materials ]
		})

search = SearchView.as_view()
