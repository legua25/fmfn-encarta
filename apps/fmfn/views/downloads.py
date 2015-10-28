# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from apps.fmfn.decorators import role_required, ajax_required
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from django.http import HttpResponseForbidden
from django.views.generic import View
from django.http import JsonResponse
from apps.fmfn.models import (
	ActionLog,
	Download,
	Material
)

class DownloadsView(View):
	"""

	"""

	@method_decorator(login_required)
	@method_decorator(role_required('teacher'))
	def get(self, request, content_id = 0):

		# Serve file

		# Save download
		try: material = Material.objects.get(id = content_id)
		except Material.DoesNotExist:

			ActionLog.objects.log_content('Failed to locate material with ID \'%s\'' % content_id, status = 403, user = request.user)
			return HttpResponseForbidden()
		else:
			Download.objects.create(
				user = request.user,
				material = material,
			)

			ActionLog.objects.log_tags('Successfully downloaded material (id: %s)' % content_id, user = request.user)




downloads = DownloadsView.as_view()