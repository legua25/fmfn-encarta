# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division
from apps.fmfn.models import (
	Material,
	ActionLog,
	Comment,
	Download,
	Portfolio
)
from django.shortcuts import RequestContext, render_to_response
from django.template.loader import render_to_string as render
from django.contrib.auth.decorators import login_required
from django.utils.translation import ugettext_lazy as _
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.contrib.auth import get_user_model
from apps.fmfn.decorators import role_required
from django.db.transaction import atomic
from django.views.generic import View
from django.utils.timezone import now
from django.http import HttpResponse
from django.db.models import *
from datetime import datetime
from math import ceil
import os, calendar

__all__ = [
	'materials',
	'users',
	'comments',
	'select'
]
User = get_user_model()

class ReportView(View):
	""" Represents a generic report view which compiles a report within a transaction to speed
		up report generation. The report is compiled once and stored in the server for history
		purposes. The report is compiled as an HTML which presents the collected data in a simple
		way. This reports may only be created by an administrator.
	"""

	report_name = ''
	report_class = None
	template = ''

	@method_decorator(login_required)
	@method_decorator(role_required('administrator'))
	# @method_decorator(cache_page(1200))
	def get(self, request):

		# Record starting time
		start = now()

		# Perform basic filters based on time range (if set)
		query = self.report_class.objects.active()

		# Extract information within a transaction
		with atomic():
			data = self.generate_report(query)

		# Render the report
		name = self.report_name
		report_doc = render(
			template_name = self.template,
			context = RequestContext(request, locals()),
			request = request
		).encode('utf-8')

		# Count the elapsed time
		time = (now() - start).total_seconds()

		# Create the report output (save it if required to)
		filename = 'report_%s.html' % calendar.timegm(start.timetuple())
		with open('reports/%s' % filename, 'w') as f:
			f.write(report_doc)

		# Send file as attachment
		ActionLog.objects.log_reports('Generated report (name: %s) in %s seconds' % ( self.report_name, time ), user = request.user)
		return HttpResponse(report_doc)

	def generate_report(self, query): raise NotImplementedError()


class MaterialReport(ReportView):

	report_name = _('Reporte de Uso de Material')
	report_class = Material
	template = 'reporting/material.html'

	def generate_report(self, query):

		month = now().month
		year = now().year

		# Determine the month range
		if 1 <= month <= 3: start, end = 1, 3
		elif 3 <= month <= 5: start, end = 3, 5
		elif 5 <= month <= 7: start, end = 5, 7
		elif 7 <= month <= 9: start, end = 7, 9
		elif 9 <= month <= 11: start, end = 9, 11
		else: start, end = 11, 1

		# Select materials based on total count
		count = int(ceil(Material.objects.active().count() * 0.10))

		filters = Q(downloads__date__range = [ datetime(year = year, month = start, day = 1), datetime(year = year, month = end, day = 1) ]) | Q(downloads__isnull = True)
		temp = query.filter(link = '').filter(filters).annotate(count = Count('downloads'))

		# Save the two queries temporarily - we must change IDs for material data
		max, min = temp.order_by('-count', 'downloads__date'), temp.order_by('count', 'downloads__date')

		# Return the two queries
		return {
			'max': max.values_list('id', 'title', 'types__name', 'count')[:count],
			'min': min.values_list('id', 'title', 'types__name', 'count')[:count]
		}

materials = MaterialReport.as_view()

class UserReport(ReportView):

	report_name = _('Reporte de Usuarios')
	report_class = User
	template = 'reporting/users.html'

	def generate_report(self, query):

		return {
			'never_logged_in': query.filter(last_login__isnull = True).values('id', 'first_name', 'father_family_name', 'mother_family_name', 'email_address', 'date_joined'),
			'never_downloaded': query.filter(downloads = None).values('id', 'first_name', 'father_family_name', 'mother_family_name', 'email_address', 'date_joined')
		}

users = UserReport.as_view()

class CommentsReport(ReportView):

	report_name = _('Reporte de Comentarios')
	report_class = Download
	template = 'reporting/comments.html'

	def generate_report(self, query):

		# date__range = [ datetime(year = year, month = start, day = 1), datetime(year = year, month = end, day = 1) ]

		today = now()
		if today.month < 7: period = Q(date__range = [ datetime(year = (today.year - 1), month = 12, day = 15), datetime(year = today.year, month = 7, day = 16) ])
		else: period = Q(date__range = [ datetime(year = today.year, month = 7, day = 16), datetime(year = today.year, month = 12, day = 15) ])

		return (query.filter(period)
		             .select_related('material')
					 .values('material')
					 .annotate(count = Count('material'))
		             .filter(material__comments = None)
		             .values_list('material__id', 'material__title', 'count'))

comments = CommentsReport.as_view()

class SelectReportView(View):


	@method_decorator(login_required)
	@method_decorator(role_required('administrator'))
	def get(self, request):
		return render_to_response('reporting/select-report.html', context = RequestContext(request, locals()))

select = SelectReportView.as_view()
