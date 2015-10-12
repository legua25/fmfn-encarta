# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase, Client
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.auth import get_user_model
from django.contrib import auth
from apps.fmfn.models import (
	SchoolGrade,
	Campus,
	Role,
	ActionLog
)

__all__ = [
	'AdminEditTest',
	'ExternalEditTest',
	'SelfEditTest'
]
User = get_user_model()

class _EditUserTest(TestCase):

	email_address = ''
	password = ''
	role = Role.objects.get(id = 1)
	should_pass = False

	fixtures = [
		'grades',
		'campus',
		'roles'
	]

	def setUp(self):

		self.client = Client(enforce_csrf_checks = False)

		user = User.objects.create_user(
			email_address = 'test@example.com',
			password = 'asdfg',
			role = Role.objects.get(id = 1),
			campus = Campus.objects.get(id = 1)
		)
		self.user_id = user.id

		if self.email_address != 'test@example.com' and self.password != 'asdfg':

			self.user = User.objects.create_user(
				email_address = self.email_address,
				password = self.password,
				role = self.role,
				campus = Campus.objects.get(id = 1)
			)
		else: self.user = user

	def test_edit_profile(self):

		self.client.login(email_address = self.email_address, password = self.password)
		response = self.client.post(reverse_lazy('users:edit', kwargs = { 'user_id': self.user_id }), data = {
			'first_name': 'John',
			'father_family_name': 'Doe'
		}, follow = True)

		if self.should_pass:

			self.assertEqual(response.status_code, 200)
			url, status = response.redirect_chain[-1]
			self.assertIn(status, [ 301, 302 ])

			user = User.objects.get(id = self.user_id)
			self.assertEqual(user.first_name, 'John')
			self.assertEqual(user.father_family_name, 'Doe')

			self.assertTrue(bool(ActionLog.objects.active()))

			log = ActionLog.objects.latest('action_date')
			self.assertEqual(log.category, 1)
			self.assertEqual(log.status, 200)
		else:

			self.assertEqual(response.status_code, 401)

			user = User.objects.get(id = self.user_id)
			self.assertNotEqual(user.first_name, 'John')
			self.assertNotEqual(user.father_family_name, 'Doe')

			self.assertTrue(bool(ActionLog.objects.active()))

			log = ActionLog.objects.latest('action_date')
			self.assertEqual(log.category, 1)
			self.assertEqual(log.status, 401)

class AdminEditTest(_EditUserTest):

	email_address = 'test_admin@example.com'
	password = 'asdfg'
	role = Role.objects.get(id = 3)
	should_pass = True

class ExternalEditTest(_EditUserTest):

	email_address = 'test2@example.com'
	password = 'asdfgh'
	should_pass = False

class SelfEditTest(_EditUserTest):

	email_address = 'test@example.com',
	password = 'asdfg'
	should_pass = True
