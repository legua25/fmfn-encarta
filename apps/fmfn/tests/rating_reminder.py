# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse_lazy
from django.test import TestCase
from django.contrib.auth import get_user_model
# from apps.fmfn.views import RatingReminder
from apps.fmfn.models import (
	Role,
	Campus,
	Material,
	Rating,
	Download,
)
#reminder = new RatingReminder instance

User = get_user_model()

class _RatingReminderTest(TestCase):
	"""

	Defines a generic test for all three tag types: Type, Theme and Language.
	Specifies a setup and tests for tag listing, creation, edition and deletion.
		-Test response status codes
		-Test object creation/edition in database
		-Test action log entries

	"""
	fixtures = [ 'grades', 'roles', 'campus' ]

	def setUp(self):
		"""
			Creates a user for login
		"""

		self.user1 = User.objects.create_user(
			email_address = 'test1@example.com',
			password = 'asdfgh',
			role = Role.objects.get(id = 4),
			campus = Campus.objects.get(id = 1)
		)

		self.user2 = User.objects.create_user(
			email_address = 'test1@example.com',
			password = 'asdfgh',
			role = Role.objects.get(id = 4),
			campus = Campus.objects.get(id = 1)
		)

		self.test_material = Material.objects.create(
								title = 'Material',
		                        description = 'Descripcion de prueba',
		                        link = 'http://blah.com'
		)

		self.test_download = Download.objects.create(
			user = self.user1,
			material = self.test_material
		)

		self.test_download = Download.objects.create(
			user = self.user2,
			material = self.test_material
		)

		self.test_rating = Rating.objects.create(
			rating_value = 5,
			material = self.test_material,
			user = self.user1
		)

	def test_users(self):
		# users = reminder.users_to_remind
		# assert user1 is in users
		# assert user2 is not in users
		pass


	def test_notifications(self):
		# Ni idea
		pass


