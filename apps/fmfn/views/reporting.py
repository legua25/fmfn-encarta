# -*- coding: utf-8 -*-
from __future__ import unicode_literals, division
from apps.fmfn.models import (
	Material,
	ActionLog,
	Comment,
	Download,
	Portfolio
)
from django.shortcuts import redirect, render_to_response, RequestContext
from django.template.loader import render_to_string as render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from apps.fmfn.decorators import role_required
from django.db.transaction import atomic
from django.views.generic import View
from django.utils.timezone import now
from django.http import HttpResponse
from django.db.models import *
from datetime import timedelta
import os

__all__ = [
	'materials'
]

class ReportView(View):

	report_type = ''
	template = ''
	store_report = True

	@method_decorator(login_required)
	@method_decorator(role_required('administrator'))
	def get(self, request):

		# Get the temporality parameter for the report
		today = now()
		target_time = (today - timedelta(days = request.GET.get('time', 1)))

		# Extract information within a transaction
		with atomic():
			report = self._generate_report(target_time)

		# Render the report
		report_doc = render(
			template_name = self.template,
			context = RequestContext(request, locals()),
			request = request
		).encode('utf-8')

		# Create the report output (save it if required to)
		filename = 'reports/report_%s.html' % today
		if ReportView.store_report:

			with open(filename, 'w') as f:
				f.write(report_doc)

			file_size = os.path.getsize(filename)

		else: file_size = len(report_doc)

		# Send file as attachment
		ActionLog.objects.log_reports('Generated report (%s)' % self.report_type, user = request.user)
		response = HttpResponse(report_doc, content_type = 'text/html')

		response['Content-Disposition'] = "attachment; filename=report_%s.html" % today
		response['Content-Length'] = file_size

		return response

	def _generate_report(self, target_time): raise NotImplementedError()


class MaterialUsageReport(ReportView):

	report_type = 'material usage report'
	template = 'reports/materials.html'

	def _generate_report(self, target_time):

		usage_ratio = (Material.objects.active().count() / Material.objects.count())
		downloads = Download.objects.active().filter(date__gte = target_time).select_related('material', 'user')

		# Most downloaded and least downloaded materials
		most_downloaded = downloads.values('material').annotate(count = Count('date', distinct = True)).order_by('-count', 'material')[:10]
		least_downloaded = downloads.values('material').annotate(count = Count('date', distinct = True)).order_by('count', 'material')[:10]

		# Apply data transformations to extract actual materials, not IDs
		with atomic():

			most_downloaded = [ Material.objects.annotate(count = Value(d['count'], output_field = IntegerField())).get(id = d['material']) for d in most_downloaded ]
			least_downloaded = [ Material.objects.annotate(count = Value(d['count'], output_field = IntegerField())).get(id = d['material']) for d in least_downloaded ]

		return {
			'usage': usage_ratio,
			'data': downloads,
			'queries': {
				'most': most_downloaded,
				'least': least_downloaded
			}
		}

materials = MaterialUsageReport.as_view()
