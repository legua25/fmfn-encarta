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
		User.objects.create_user(
			email_address = 'test1@example.com',
			password = 'asdfgh',
			role = Role.objects.get(id = 2),
			campus = Campus.objects.get(id = 1)
		)

		# Create the material to add
		self.content_id = Material.objects.create(
			title = 'Test',
			description = 'Mary had a little lamb... blah, blah, blah',
			link = 'http://localhost/',
			user = User.objects.create_user(
				email_address = 'test2@example.com',
				password = 'asdfgh',
				role = Role.objects.get(id = 4),
				campus = Campus.objects.get(id = 1)
			)
		).id

	def test_material_added(self):

		log_size = ActionLog.objects.active().count()

		self.client.login(email_address = 'test1@example.com')
		response = self.client.put(reverse_lazy('portfolio:edit', kwargs = { 'content_id': self.content_id }), follow = True)

	def test_repeated_material(self):

		log_size = ActionLog.objects.active().count()

		self.client.login(email_address = 'test1@example.com')
		response = self.client.put(reverse_lazy('portfolio:edit', kwargs = { 'content_id': self.content_id }), follow = True)
	def test_removed_material(self):

		log_size = ActionLog.objects.active().count()

		self.client.login(email_address = 'test1@example.com')
		response = self.client.delete(reverse_lazy('portfolio:edit', kwargs = { 'content_id': self.content_id }), follow = True)
	def test_removed_twice(self):

		log_size = ActionLog.objects.active().count()

		self.client.login(email_address = 'test1@example.com')
		response = self.client.delete(reverse_lazy('portfolio:edit', kwargs = { 'content_id': self.content_id }), follow = True)
