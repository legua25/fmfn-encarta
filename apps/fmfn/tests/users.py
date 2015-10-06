# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.test import TestCase, Client

__all__ = [ 'CreateUserTest' ]
User = get_user_model()

class CreateUserTest(TestCase):

	def setUp(self):
		self.client = Client(enforce_csrf_checks = False)

	def test_taken_email(self):

		User.objects.create_user(username = 'test1@example.com', email = 'test1@example.com', password = 'asdfg123')
		response = self.client.post(reverse_lazy('users:create'), data = {
			'email_address': 'test1@example.com',
			'password': 'asdfgh123'
		}, follow = True)


	def test_no_role_given(self): pass
	def test_insert_user(self): pass
	def test_valid_profile(self): pass
