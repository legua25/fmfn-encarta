# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse_lazy
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from apps.fmfn.models import (
	Material,
	Role,
	Campus,
	Report,
	ActionLog
)

User = get_user_model()

class ReportsTest(TestCase):
	"""

	Specifies a setup and tests for report listing, creation, rejection and resolution
		-Test response status codes
		-Test object creation/edition in database
		-Test action log entries

	"""

	fixtures = [ 'grades', 'roles', 'campus' ]


	def setUp(self):
		"""
			Creates an AJAX client for processing requests and a user user for login
		"""

		# Create AJAX request client
		self.client = Client(
			enforce_csrf_checks = False,
			HTTP_X_REQUESTED_WITH = 'XMLHttpRequest'
		)

		# Create user
		self.user = User.objects.create_user(
			email_address = 'test1@example.com',
			password = 'asdfgh',
			role = Role.objects.get(id = 4),
			campus = Campus.objects.get(id = 1)
		)

	def _action_log_tests(self, log_count, status):
		"""
			Test new object creation in log and correctness of category and status code
		"""

		self.assertEqual(len(ActionLog.objects.active()), (log_count + 1))
		self.assertEqual(ActionLog.objects.latest('action_date').category, 6)
		self.assertEqual(ActionLog.objects.latest('action_date').status, status)

	def _create_material(self):
		"""
			Initializes a test material and report and log counters
		"""
		self.report_count = len(Report.objects.active())
		self.log_count = len(ActionLog.objects.active())
		self.assertEqual(self.report_count, 0)

		# Create test material
		self.material = Material.objects.create(
								title = 'Material de prueba',
								description = 'Descripcion de prueba',
								link = 'http://blah.com'
		)


	def test_report_material(self):
		"""

			Generates a post request with new report information.
				-Asserts the response status code, database and action log are as expected

		"""

		# Setup test
		self._create_material()

		# Create a report for created test material
		self.client.login(email_address = 'test1@example.com', password = 'asdfgh')
		response = self.client.post(reverse_lazy('management:create', kwargs = { 'content_id': self.material.id }), data = {
			'description': 'broken'
		}, follow = True)

		# Check status code
		self.assertEqual(response.status_code, 201)

		# Check report is crated on database
		self.assertEqual(len(Report.objects.active()), (self.report_count + 1))

		# Check action log
		self._action_log_tests(self.log_count, 201)

	def test_report_nonexistent_material(self):
		"""

			Generates a report post request for a material that doesn't exist
				-Asserts the response status code, database and action log are as expected

		"""

		# Setup test
		self._create_material()

		# Create a report for a nonexistent material (id = 0)
		self.client.login(email_address = 'test1@example.com', password = 'asdfgh')
		response = self.client.post(reverse_lazy('management:create', kwargs = { 'content_id': 0 }), data = {
			'description': 'broken'
		}, follow = True)

		# Check status code
		self.assertEqual(response.status_code, 403)

		# Check report is NOT crated on database
		self.assertEqual(len(Report.objects.active()), (self.report_count))

		# Check action log
		self._action_log_tests(self.log_count, 403)

	def test_report_material_twice(self):
		"""

			Generates a report post request for a material that has already been reported by user
				-Asserts the response status code, database and action log are as expected

		"""

		# Setup test
		self._create_material()

		# Create another report for created test material
		self.client.login(email_address = 'test1@example.com', password = 'asdfgh')
		response = self.client.post(reverse_lazy('management:create', kwargs = { 'content_id': self.material.id }), data = {
			'description': 'bad'
		}, follow = True)

		# Check status code
		self.assertEqual(response.status_code, 201)

		# Check report is crated on database
		self.assertEqual(len(Report.objects.active()), (self.report_count + 1))

		# Check action log
		self._action_log_tests(self.log_count, 201)

	def test_list_reports(self):
		"""
			Generates a get request of all reports currently in progress
				-Asserts response status code and action log are as expected

		"""

		# Initializes log counter
		log_count = len(ActionLog.objects.active())

		# Create request
		self.client.login(email_address = 'test1@example.com', password = 'asdfgh')
		response = self.client.get(reverse_lazy('management:list'), follow = True)

		# Check status code
		self.assertEqual(response.status_code, 200)

		# Check action log
		self._action_log_tests(log_count, 200)

	def test_resolve_report(self):
		"""
			Generates a patch request that updates the post to resolved status
				-Asserts the response status code, database and action log are as expected

		"""

		# Setup test
		self._create_material()

		# Create new report for test material
		report = Report.objects.create(user = self.user, description = 'test', material = self.material, status=1)

		# Resolve the created report
		self.client.login(email_address = 'test1@example.com', password = 'asdfgh')
		response = self.client.patch(reverse_lazy('management:manage', kwargs = { 'report_id': report.id }), follow = True)

		# Check status code
		self.assertEqual(response.status_code, 200)

		# Check report changes in database
		self.assertEqual(Report.objects.filter(status = '2').count(), 1)

		# Check action log
		self._action_log_tests(self.log_count, 201)

	def test_reject_report(self):
		"""
			Generates a delete request that updates the post to rejected status
				-Asserts the response status code, database and action log are as expected

		"""
		# Setup test
		self._create_material()

		# Create new report for test material
		report = Report.objects.create(user = self.user, description = 'test', material = self.material, status=1)

		# Reject the created report
		self.client.login(email_address = 'test1@example.com', password = 'asdfgh')
		response = self.client.delete(reverse_lazy('management:manage', kwargs = { 'report_id': report.id }), follow = True)

		# Check status code
		self.assertEqual(response.status_code, 200)

		# Check report changes in database
		self.assertEqual(Report.objects.filter(status = '4').count(), 1)

		# Check action log
		self._action_log_tests(self.log_count, 201)
