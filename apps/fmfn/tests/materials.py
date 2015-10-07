# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse_lazy
from apps.fmfn.models import ActionLog, Material
from django.contrib.auth import get_user_model
from django.test import TestCase, Client

__all__ = ['CreateMaterialTest', 'EditMaterialTest', 'DeleteMaterialTest']
User = get_user_model()

class CreateMaterialTest(TestCase):

	fixtures = [ 'grades' ]

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
			'suggested_ages': 1,
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
			'suggested_ages': 1,
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
			'suggested_ages': 1,
			'user': User.objects.get(email_address = 'test1@example.com').id
		}
		response = self.client.post(reverse_lazy('content:create'), data = mock_data, follow = True)

		# 302 status means the system redirected the user successfully
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.redirect_chain[-1], 302)

		# checking that the latest record's info matches the input
		latest = Material.objects.get(id = 1)

		self.assertEqual(latest.title, mock_data['title'])
		self.assertEqual(latest.description, mock_data['description'])
		self.assertEqual(latest.link, mock_data['link'])
		self.assertEqual(latest.suggested_ages, mock_data['suggested_ages'])
		self.assertEqual(latest.user, mock_data['description'])

		self.assertEqual(len(ActionLog.objects.active()), 1)
		self.assertEqual(ActionLog.objects.latest('action_date').category, 2)
		self.assertEqual(ActionLog.objects.latest('action_date').status, 302)

class EditMaterialTest(TestCase):

	def setUp(self):

		self.client = Client(enforce_csrf_checks = False)

		# Create test users
		# active user
		self.user = User.objects.create_user(
			email_address = 'test1@example.com',
			password = 'asdfg123'
		)
		Material.objects.create(
			title = 'Actividad de Español II',
			description = 'Descripción de material español',
			link = 'http://facebook.com',
			suggested_ages = 1,
			user = self.user
		)

	def test_material_edited(self):

		self.client.login(email_address = 'test1@example.com', password = 'asdfg123')
		data = {
			'title': 'Matemáticas II',
	        'description': 'Descripción de material 1 edit',
	        'link': 'http://www.google.com.mx',
	        'suggested_ages': 1,
	        'user': self.user.id
		}
		response = self.client.post(reverse_lazy('content:edit', kwargs = { 'content_id': 1 }), data)

		record = Material.objects.get(id = 1)
		self.assertEqual(response.status_code, 302)
		self.assertEqual(record.title, data['title'])
		self.assertEqual(record.description, data['description'])
		self.assertEqual(record.link, data['link'])
		self.assertEqual(ActionLog.objects.latest('action_date').category, 2)
		self.assertEqual(ActionLog.objects.latest('action_date').status, 302)

class DeleteMaterialTest(TestCase):

	def setUp(self):

		self.client = Client()

		user = User.objects.create_user(
			email_address = 'test1@example.com',
			password = 'asdfg123'
		)
		Material.objects.create(
			title = 'Actividad de Español II',
			description = 'Descripción de material español',
			link = 'http://facebook.com',
			suggested_ages = 1,
			user = user
		)

	def test_material_deleted(self):

		self.client.login(email_address = 'test1@example.com', password = 'asdfg123')
		response = self.client.delete(reverse_lazy('content:edit', kwargs = { 'content_id': 1 }))

		self.assertEqual(response.status_code, 302)
		self.assertEqual(Material.objects.get(id = 1).active, False)
		self.assertEqual(ActionLog.objects.latest('action_date').category, 2)
		self.assertEqual(ActionLog.objects.latest('action_date').status, 302)
