# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse_lazy
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from apps.fmfn.models import (
	Type,
	Theme,
	Language,
	Role,
	Campus,
	ActionLog
)

__all__ = [
	'TypeTagTest',
	'ThemeTagTest',
	'LanguageTagTest'
]
User = get_user_model()

class _TagTest(TestCase):
	"""

	Defines a generic test for all three tag types: Type, Theme and Language.
	Specifies a setup and tests for tag listing, creation, edition and deletion.
		-Test response status codes
		-Test object creation/edition in database
		-Test action log entries

	"""
	tag_class = Type
	fixtures = [ 'grades', 'roles', 'campus' ]

	@property
	def tag_name(self): return self.tag_class.__name__.lower()

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
		self.assertEqual(ActionLog.objects.latest('action_date').category, 4)
		self.assertEqual(ActionLog.objects.latest('action_date').status, status)

	def test_create_new_tag(self):
		"""

			Generates a post request with new tag information.
				-Asserts the response status code, database and action log are as expected
			Generates a post request with existing tag information.
				-Asserts the response status code is correct

		"""
		tag_count = len(self.tag_class.objects.active())
		log_count = len(ActionLog.objects.active())
		self.assertEqual(tag_count, 0)

		# Test case: a tag creation request arrives
		self.client.login(email_address = 'test1@example.com', password = 'asdfgh')
		response = self.client.post(reverse_lazy('tags:create'), data = {
			'type': self.tag_name,
			'name': 'philosophy'
		}, follow = True)

		# Check status code
		self.assertEqual(response.status_code, 201)

		# Check material count
		self.assertEqual(len(self.tag_class.objects.active()), (tag_count + 1))

		# Check action log
		self._action_log_tests(log_count, 201)

		# Test case: a repeated tag creation request arrives
		self.tag_class.objects.create(name = 'test')
		log_count = len(ActionLog.objects.active())

		self.client.login(email_address = 'test1@example.com', password = 'asdfgh')
		response = self.client.post(reverse_lazy('tags:create'), data = {
			'type': self.tag_name,
			'name': 'test'
		})

		# Check status code
		self.assertEqual(response.status_code, 302)

		# Check action log
		self._action_log_tests(log_count, 302)

	def test_list_tags(self):
		"""
			Generates a get request specifying a tag type
				-Asserts response status code and action log are as expected

		"""
		log_count = len(ActionLog.objects.active())
		self.client.login(email_address = 'test1@example.com', password = 'asdfgh')
		response = self.client.get(reverse_lazy('tags:list'), data = {
			'type': self.tag_name,
		}, follow = True)

		# Check status code
		self.assertEqual(response.status_code, 200)

		# Check action log
		self._action_log_tests(log_count, 200)
	def test_list_filtered_tags(self):
		"""
			Generates a get request specifying a tag type and filter pattern
				-Asserts response status code and action log are as expected

		"""

		log_count = len(ActionLog.objects.active())
		self.client.login(email_address = 'test1@example.com', password = 'asdfgh')
		response = self.client.get(reverse_lazy('tags:list'), data = {
			'type': self.tag_name,
			'filter': 'tag'
		}, follow = True)

		# Check status code
		self.assertEqual(response.status_code, 200)

		# Check action log
		self._action_log_tests(log_count, 200)
	def test_edit_tag(self):
		"""
			Generates a post request specifying a tag id and a new name
				-Asserts the response status code, database and action log are as expected

		"""

		log_count = len(ActionLog.objects.active())
		tag = self.tag_class.objects.create(name = 'test')

		self.client.login(email_address = 'test1@example.com', password = 'asdfgh')
		response = self.client.post(reverse_lazy('tags:edit', kwargs = { 'tag_type': self.tag_name, 'tag_id': tag.id }), data = {
			'name': 'test1',
		}, follow = True)

		# Check status code
		self.assertEqual(response.status_code, 200)

		# Check tag changes
		self.assertEqual(len(self.tag_class.objects.filter(name = 'test1')), 1)

		# Check action log
		self._action_log_tests(log_count, 201)
	def test_delete_tag(self):
		"""
			Generates a post request specifying a tag id and a new name
				-Asserts the response status code, database and action log are as expected

		"""

		tag = self.tag_class.objects.create(name = 'test')
		log_count = len(ActionLog.objects.active())
		tag_count = len(self.tag_class.objects.active())

		# Test case: a tag creation request arrives
		self.client.login(email_address = 'test1@example.com', password = 'asdfgh')
		response = self.client.delete(reverse_lazy('tags:edit', kwargs = { 'tag_type': self.tag_name, 'tag_id': tag.id }), follow = True)

		# Check status code
		self.assertEqual(response.status_code, 200)

		# Check material count
		self.assertEqual(len(self.tag_class.objects.active()), (tag_count - 1))

		# Check action log
		self._action_log_tests(log_count, 200)

class TypeTagTest(_TagTest):
	tag_class = Type
class ThemeTagTest(_TagTest):
	tag_class = Theme
class LanguageTagTest(_TagTest):
	tag_class = Language
