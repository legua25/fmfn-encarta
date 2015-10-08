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

__all__ = [
	'MaterialTest'
]
User = get_user_model()

class MaterialTest(TestCase):

	fixtures = [ 'roles', 'grades', 'campus' ]

	def setUp(self):

		self.client = Client(enforce_csrf_checks = False)
		self.user = User.objects.create_user(
			email_address = 'test1@example.com',
			password = 'asdfgh',
			role = Role.objects.get(id = 4),
			campus = Campus.objects.get(id = 1)
		)

	def test_material_created(self):

		material_count = len(Material.objects.active())

		# Test case: a valid submission arrives
		self.client.login(email_address = 'test1@example.com', password = 'asdfgh')
		response = self.client.post(reverse_lazy('content:create'), data = {
			'title': 'A material test',
			'description': 'This material works best for testing purposes',
			'link': 'http://127.0.0.1:8000/search/',
			'languages': Language.objects.active().filter(id = 1),
			'suggested_ages': [ g.id for g in SchoolGrade.objects.filter(id__in = [ 3, 4 ]) ]
		}, follow = True)

		# Check the response status sequence
		self.assertEqual(response.status_code, 200)
		url, status = response.redirect_chain[-1]
		self.assertEqual(status, 302)

		# Check the materials count increased by one
		self.assertEqual(len(Material.objects.active()), (material_count + 1))

		# Check the action log
		self.assertTrue(bool(ActionLog.objects.active()))
		self.assertEqual(len(ActionLog.objects.active()), 1)
		self.assertEqual(ActionLog.objects.latest('action_date').category, 2)
		self.assertEqual(ActionLog.objects.latest('action_date').status, 201)
	def test_material_edited(self): pass
	def test_material_deleted(self):

		material = Material.objects.create(
			title = 'Test material',
			description = 'A material destined to test deletion',
			link = 'http://127.0.0.1:8000/',
			user = self.user
		)
		material_count = len(Material.objects.active())
		material_id = material.id

		# Test case: a valid submission arrives
		self.client.login(email_address = 'test1@example.com', password = 'asdfgh')
		response = self.client.delete(reverse_lazy('content:edit', kwargs = { 'content_id': material_id }), follow = True)

		# Check the response status sequence
		self.assertEqual(response.status_code, 200)

		# Test the document schema
		self.assertJSONEqual(str(response.content), {
			'version': '1.0.0',
			'status': 200,
			'material': { 'id': material_id, 'status': 'delete' }
		})

		# Check the materials count increased by one
		self.assertEqual(len(Material.objects.active()), (material_count - 1))

		# Check the action log
		self.assertTrue(bool(ActionLog.objects.active()))
		self.assertEqual(len(ActionLog.objects.active()), 1)
		self.assertEqual(ActionLog.objects.latest('action_date').category, 2)
		self.assertEqual(ActionLog.objects.latest('action_date').status, 200)
