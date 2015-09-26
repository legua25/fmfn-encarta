# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse_lazy
from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from apps.fmfn.views import login

__all__ = [ 'LoginTest' ]
User = get_user_model()

class LoginTest(TestCase):

	def setUp(self):

		# Create a request factory
		self.factory = RequestFactory()

		# Create a test user
		User.objects.create_user(
			username = 'email@example.com',
			email = 'email@example.com',
			password = 'asdfg123'
		)

	def test_login_invalid_user(self):

		# Create a mock request (type: POST, arguments from actual form)
		request = self.factory.post(reverse_lazy('index'), data = {
			'email': 'a@a.com',
			'password': 'asdfg123'
		})
		request.user = None

		# Executes the view code, builds response
		response = login(request)
		# Upon failure, status code is 401 - test this
		self.assertEqual(response.status_code, 401)
	def test_login_valid_user(self):

		# Create a mock request (type: POST, arguments from actual form)
		request = self.factory.post(reverse_lazy('index'), data = {
			'email': 'email@example.com',
			'password': 'asdfg123'
		})
		request.user = None

		# Executes the view code, builds response
		response = login(request)
		# User is redirected upon successful login - verify this by status code 301
		self.assertEqual(response.status_code, 301)
	def test_already_logged_in(self):

		# Create a mock request (type: POST, arguments from actual form)
		request = self.factory.post(reverse_lazy('index'))
		request.user = User.objects.get(email = 'email@example.com')

		# Executes the view code, builds response
		response = login(request)
		# User is redirected upon successful login - verify this by status code 301
		self.assertEqual(response.status_code, 301)
