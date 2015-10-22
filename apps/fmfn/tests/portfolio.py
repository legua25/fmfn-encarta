# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from apps.fmfn.models import (
	Portfolio,
	Material,
	Role,
	Campus,
	Language,
	ActionLog
)

__all__ = [ 'PortfolioTest' ]
User = get_user_model()

class PortfolioTest(TestCase):

	fixtures = [ 'roles', 'campus', 'languages' ]

	def setUp(self):

		self.client = Client(
			enforce_csrf_checks = False,
			HTTP_X_REQUESTED_WITH = 'XMLHttpRequest'
		)

		# Create our test users
		self.user = User.objects.create_user(
			email_address = 'test1@example.com',
			password = 'asdfgh',
			role = Role.objects.get(id = 2),
			campus = Campus.objects.get(id = 1)
		)

		# Create the material to add
		self.material = Material.objects.create(
			title = 'Test',
			description = 'Mary had a little lamb... blah, blah, blah',
			link = 'http://localhost/',
			user = User.objects.create_user(
				email_address = 'test2@example.com',
				password = 'asdfgh',
				role = Role.objects.get(id = 4),
				campus = Campus.objects.get(id = 1)
			)
		)

	def test_material_added(self):

		log_size = ActionLog.objects.active().count()

		self.client.login(email_address = 'test1@example.com', password = 'asdfgh')
		response = self.client.put(reverse_lazy('portfolio:edit', kwargs = { 'content_id': self.material.id }), follow = True)

		self.assertEqual(response.status_code, 201)
		portfolio = Portfolio.objects.user(self.user)
		self.assertEqual(portfolio.items.all().count(), 1)
		self.assertJSONEqual(str(response.content), {
			'version': '1.0.0',
			'status': 201,
			'material': {
				'id': self.material.id,
				'title': self.material.title,
				'description': self.material.description,
				'content': None,
				'link': self.material.link
			}
		})

		self.assertEqual(ActionLog.objects.active().count(), (log_size + 1))
		log = ActionLog.objects.latest('action_date')
		self.assertEqual(log.category, 2)
		self.assertEqual(log.status, 201)
	def test_repeated_material(self):

		log_size = ActionLog.objects.active().count()

		self.client.login(email_address = 'test1@example.com', password = 'asdfgh')
		self.client.put(reverse_lazy('portfolio:edit', kwargs = { 'content_id': self.material.id }), follow = True)
		response = self.client.put(reverse_lazy('portfolio:edit', kwargs = { 'content_id': self.material.id }), follow = True)

		self.assertEqual(response.status_code, 403)
		portfolio = Portfolio.objects.user(self.user)
		self.assertEqual(portfolio.items.all().count(), 1)

		self.assertEqual(ActionLog.objects.active().count(), (log_size + 2))
		log = ActionLog.objects.latest('action_date')
		self.assertEqual(log.category, 2)
		self.assertEqual(log.status, 403)
	def test_removed_material(self): pass
	def test_removed_twice(self): pass
