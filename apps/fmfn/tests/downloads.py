# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse_lazy
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from apps.fmfn.models import (
	Role,
	Campus,
	Download,
	Material,
	ActionLog
)

User = get_user_model()

class DownloadsTest(TestCase):
	"""
	"""

	def setUp(self):
		"""
		"""

		# Create client
		self.client = Client(
			enforce_csrf_checks = False
		)

		# Create user
		self.user = User.objects.create_user(
			email_address = 'test1@example.com',
			password = 'asdfgh',
			role = Role.objects.get(id = 4),
			campus = Campus.objects.get(id = 1)
		)

		# Create material to download
		self.material = Material.objects.create(
								title = 'Material a editar',
								description = 'Descripcion de prueba',
								link = 'http://blah.com'
		)

	def test_download(self):
		download_count = len(Download.objects.active())
		log_count = len(ActionLog.objects.active())
		self.assertEqual(download_count, 0)


		self.client.login(email_address = 'test1@example.com', password = 'asdfgh')

		response = self.client.get(reverse_lazy('content:download',kwargs={'content_id':self.material.id}))

		# Check status code
		self.assertEqual(response.status_code, 201)

		# Check material count
		self.assertEqual(len(Download.objects.active()), (download_count + 1))

		# Check action log
		self._action_log_tests(log_count, 201)