__author__ = 'LuisE'

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from apps.fmfn.models import (
	ActionLog,
	Material,
	Role,
	Campus,
	Language,
	SchoolGrade
)
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
import os

__all__ = [
	'MaterialTest'
]
User = get_user_model()

class MaterialTest(TestCase):
	""" Material Search tests:
		- test_material_created: basic material creation flow
	"""

	fixtures = [ 'roles', 'grades', 'campus']

	def setUp(self):

		self.client = Client(enforce_csrf_checks = False)
		self.user = User.objects.create_user(
			email_address = 'test1@example.com',
			password = 'asdfgh',
			role = Role.objects.get(id = 5),
			campus = Campus.objects.get(id = 1)
		)

	def test_search_filters_no_match(self):
		""" After executing content/create function, verifies that:
			- the http responses are successful
			- the ActionLog contains the latest operation registry
			- the latest entry in the log contains a 200 response code
			- returns no content
		"""

		Material.objects.create(
			title = 'Material uno',
			description = 'Descripcion de prueba',
			link = 'http://blah.com'
		)

		Material.objects.create(
			title = 'Material dos',
			description = 'Descripcion',
			link = 'http://blah.com'
		)

		Material.objects.create(
			title = 'Material tres',
			description = 'Descripcion',
			link = 'http://blah.com'
		)

		log_count = len(ActionLog.objects.active())
		self.client.login(email_address = 'test1@example.com', password = 'asdfgh')
		response = self.client.get(reverse_lazy('search:filter', data = { 'filter': 'ciencia' }, follow = True))

		# Check status code
		self.assertEqual(response.status_code, 204)

		# Check action log
		# Check the action log
		self.assertTrue(bool(ActionLog.objects.active()))
		self.assertEqual(len(ActionLog.objects.active()), (log_count + 1))
		self.assertEqual(ActionLog.objects.latest('action_date').category, 4)
		self.assertEqual(ActionLog.objects.latest('action_date').status, 200)

	def test_search_filters_match(self):
		""" After executing content/create function, verifies that:
			- the http responses are successful
			- the ActionLog contains the latest operation registry
			- the latest entry in the log contains a 200 response code
			- returns matched elements
		"""

		Material.objects.create(
			title = 'Material uno',
			description = 'Descripcion de prueba',
			link = 'http://blah.com'
		)

		Material.objects.create(
			title = 'Material dos',
			description = 'Descripcion',
			link = 'http://blah.com'
		)

		Material.objects.create(
			title = 'Material tres',
			description = 'Descripcion',
			link = 'http://blah.com'
		)

		log_count = len(ActionLog.objects.active())
		self.client.login(email_address = 'test1@example.com', password = 'asdfgh')
		response = self.client.get(reverse_lazy('search:filter', data = { 'filter': 'material' }, follow = True))

		# Check status code
		self.assertEqual(response.status_code, 200)

		# Check action log
		# Check the action log
		self.assertTrue(bool(ActionLog.objects.active()))
		self.assertEqual(len(ActionLog.objects.active()), (log_count + 1))
		self.assertEqual(ActionLog.objects.latest('action_date').category, 4)
		self.assertEqual(ActionLog.objects.latest('action_date').status, 200)