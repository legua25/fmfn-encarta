# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from apps.fmfn.models import ActionLog, Material, Role
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.test import TestCase, Client

__all__ = [
	'CreateMaterialTest',
	'EditMaterialTest',
	'DeleteMaterialTest'
]
User = get_user_model()

class CreateMaterialTest(TestCase):

	fixtures = [ 'grades', 'roles', 'campus' ]

	def setUp(self):

		self.client = Client(enforce_csrf_checks = False)

		# Create test users
		# active user
		User.objects.create_user(
			email_address = 'test1@example.com',
			password = 'asdfg123'
		)
		User.objects.create_user(
			email_address = 'test2@example.com',
			password = 'asdfg123',
			active = False
		)

		ActionLog.objects.all().delete()

	def test_inactive_user(self):

		self.client.login(email_address = 'test2@example.com', password = 'asdfg123')

		# Test case: an inactive user attempts to add content
		response = self.client.post(reverse_lazy('content:create'), data = {
			'title': 'Matemáticas I',
			'description': 'Descripción de material 1',
			'link': 'http://www.google.com',
			'user': User.objects.get(email_address = 'test2@example.com').id
		}, follow = True)

		# response 401 - unauthorized
		self.assertEqual(response.status_code, 401)
		self.assertEqual(ActionLog.objects.latest('action_date').category, 2)
		self.assertEqual(ActionLog.objects.latest('action_date').status, 401)
	def test_empty_submission(self):

		self.client.login(email_address = 'test1@example.com', password = 'asdfg123')

		# Test case: empty material submission incoming
		response = self.client.post(reverse_lazy('content:create'), data = {
			'description': 'Descripción de material 1',
			'user': User.objects.get(email_address = 'test1@example.com').id
		}, follow = True)

		self.assertEqual(response.status_code, 401)

		self.assertTrue(bool(Material.objects.active()) is False)

		self.assertEqual(len(ActionLog.objects.active()), 1)
		self.assertEqual(ActionLog.objects.latest('action_date').category, 2)
		self.assertEqual(ActionLog.objects.latest('action_date').status, 401)
	def test_material_created(self):

		self.client.login(email_address = 'test1@example.com', password = 'asdfg123')

		# Test case: valid material submission incoming
		mock_data = {
			'title': 'Matemáticas I',
			'description': 'Descripción de material 1',
			'link': 'http://www.google.com',
			'user': User.objects.get(email_address = 'test1@example.com')
		}
		response = self.client.post(reverse_lazy('content:create'), data = mock_data, follow = True)

		# 301 status means the system redirected the user successfully
		self.assertEqual(response.status_code, 200)
		url, status = response.redirect_chain[-1]
		self.assertEqual(status, 301)

		# checking that the latest record's info matches the input
		latest = list(reversed(Material.objects.active()))[0]

		self.assertEqual(latest.title, mock_data['title'])
		self.assertEqual(latest.description, mock_data['description'])
		self.assertEqual(latest.link, mock_data['link'])
		self.assertEqual(latest.suggested_ages, mock_data['suggested_ages'])
		self.assertEqual(latest.user, mock_data['description'])

		self.assertEqual(len(ActionLog.objects.active()), 1)
		self.assertEqual(ActionLog.objects.latest('action_date').category, 2)
		self.assertEqual(ActionLog.objects.latest('action_date').status, 201)
class EditMaterialTest(TestCase):

	fixtures = [ 'grades', 'roles', 'campus' ]

	def setUp(self):

		self.client = Client(enforce_csrf_checks = False)

		self.user = User.objects.create_user(
			email_address = 'test1@example.com',
			password = 'asdfg123',
			role = Role.objects.get(id = 4)
		)
		self.material = Material.objects.create(
			title = 'Actividad de Español II',
			description = 'Descripción de material español',
			link = 'http://facebook.com',
			user = self.user
		)

	def test_material_edited(self):

		self.client.login(email_address = 'test1@example.com', password = 'asdfg123')
		data = {
			'title': 'Matemáticas II',
	        'description': 'Descripción de material 1 edit',
	        'link': 'http://www.google.com.mx',
	        'user': self.user
		}
		response = self.client.post(reverse_lazy('content:edit', kwargs = { 'content_id': self.material.id }), data = data, follow = True)

		# Redirection should have taken place - test this
		self.assertEqual(response.status_code, 200)

		# Material should have been soft-deleted
		self.material.refresh_from_db()
		self.assertEqual(self.material.title, data['title'])
		self.assertEqual(self.material.description, data['description'])
		self.assertEqual(self.material.link, data['link'])

		# Test action log
		self.assertEqual(len(ActionLog.objects.active()), 1)
		self.assertEqual(ActionLog.objects.latest('action_date').category, 2)
		self.assertEqual(ActionLog.objects.latest('action_date').status, 302)
class DeleteMaterialTest(TestCase):

	fixtures = [ 'grades', 'roles', 'campus' ]

	def setUp(self):

		self.client = Client(enforce_csrf_checks = False)

		user = User.objects.create_user(
			email_address = 'test1@example.com',
			password = 'asdfg123',
			role = Role.objects.get(id = 4)
		)
		self.material = Material.objects.create(
			title = 'Actividad de Español II',
			description = 'Descripción de material español',
			link = 'http://facebook.com',
			user = user
		)

	def test_material_deleted(self):

		self.client.login(email_address = 'test1@example.com', password = 'asdfg123')
		response = self.client.delete(reverse_lazy('content:edit', kwargs = { 'content_id': self.material.id }), follow = True)

		# Redirection should have taken place - test this
		self.assertEqual(response.status_code, 200)
		url, status = response.redirect_chain[-1]
		self.assertEqual(status, 302)

		# Material should have been soft-deleted
		self.material.refresh_from_db()
		self.assertFalse(self.material.active)

		# Test action log
		self.assertEqual(len(ActionLog.objects.active()), 1)
		self.assertEqual(ActionLog.objects.latest('action_date').category, 2)
		self.assertEqual(ActionLog.objects.latest('action_date').status, 200)
