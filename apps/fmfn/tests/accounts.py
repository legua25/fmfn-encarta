# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.test import TestCase, Client

__all__ = [ 'LoginTest' ]
User = get_user_model()

class LoginTest(TestCase):

	def setUp(self):

		# Create a request factory
		self.client = Client()

		# Create a test user
		User.objects.create_user(
			username = 'email@example.com',
			email = 'email@example.com',
			password = 'asdfg123'
		)

	def test_login_invalid_user(self):

		# Create a mock request (type: POST, arguments from actual form)
		response = self.client.post(reverse_lazy('login'), data = {
			'email': 'a@a.com',
			'password': 'asdfg123'
		})

		# Upon failure, status code is 401 - test this
		self.assertEqual(response.status_code, 401)
	def test_login_valid_user(self):

		# Create a mock request (type: POST, arguments from actual form)
		response = self.client.post(reverse_lazy('login'), data = {
			'email': 'email@example.com',
			'password': 'asdfg123'
		})

		# User is redirected upon successful login - verify this by status code 302
		self.assertEqual(response.status_code, 302)
	def test_already_logged_in(self):

		# Create a mock request (type: POST, arguments from actual form)
		response = self.client.post(reverse_lazy('login'), data = {
			'email': 'email@example.com',
			'password': 'asdfg123'
		})

		# User is redirected upon successful login - verify this by status code 302
		self.assertEqual(response.status_code, 302)

		# User is redirected because he/she is already logged in - verify this by status code 302
		response = self.client.post(reverse_lazy('login'))
		self.assertEqual(response.status_code, 302)
