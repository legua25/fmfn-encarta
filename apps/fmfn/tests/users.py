# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.test import TestCase, Client
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.auth import get_user_model
from apps.fmfn.models import (
	SchoolGrade,
	Campus,
	Role,
	ActionLog
)

__all__ = [
	'ExternalUserTest',
	'AdminUserTest',
	'SelfUserTest'
]
User = get_user_model()

class _UserTest(TestCase):
	"""
		Class containing a collection of tests which verify that user roles limitations are effectively applied on certain modules.
			It assumes that certain grades, campus and roles have been previously defined in the system.
	"""
	email_address = ''
	password = ''
	role = Role.objects.get(id = 2)
	should_pass = False
	should_pass_delete = False
	use_self = False

	fixtures = [
		'grades',
		'campus',
		'roles'
	]

	def setUp(self):

		self.client = Client(
			enforce_csrf_checks = False,
			HTTP_X_REQUESTED_WITH = 'XMLHttpRequest'
		)

		user = User.objects.create_user(
			email_address = 'test@example.com',
			password = 'asdfg',
			role = Role.objects.get(id = 2),
			campus = Campus.objects.get(id = 1)
		)
		self.user_id = user.id

		if not self.use_self:

			self.user = User.objects.create_user(
				email_address = self.email_address,
				password = self.password,
				role = self.role,
				campus = Campus.objects.get(id = 1)
			)
		else: self.user = user

		self.client.login(email_address = self.email_address, password = self.password)

	def test_edit_profile(self):
		"""
			Test which verifies that roles allowed to edit other users are effectively able to,
			otherwise, that a 40x is replied.
		"""
		user_target = User.objects.get(id = self.user_id)

		with open('./media/users/test.jpg') as f:

			response = self.client.post(reverse_lazy('users:edit', kwargs = { 'user_id': self.user_id }), data = {
				'first_name': 'John',
				'mother_family_name': user_target.mother_family_name,
				'father_family_name': 'Doe',
				'photo': f,
				'email_address': user_target.email_address,
				'role': user_target.role.id,
				'campus': user_target.campus.id,
				'password': self.password,
				'repeat': self.password
			}, follow = True)

		if self.should_pass:

			self.assertEqual(response.status_code, 200)

			url, status = response.redirect_chain[-1]
			self.assertIn(status, [ 301, 302 ])

			user = User.objects.get(id = self.user_id)

			# Advanced form should accept these changes:
			if self.user.belongs_to('user manager'):

				self.assertEqual(user.first_name, 'John')
				self.assertEqual(user.father_family_name, 'Doe')
			else:

				# Basic form should not accept these changes:
				self.assertNotEqual(user.first_name, 'John')
				self.assertNotEqual(user.father_family_name, 'Doe')

			# Both should accept this change:
			self.assertNotEqual(user.photo.name, 'users/default.png')

			self.assertTrue(bool(ActionLog.objects.active()))

			log = ActionLog.objects.latest('action_date')
			self.assertEqual(log.category, 1)
			self.assertEqual(log.status, 200)
		else:

			self.assertIn(response.status_code, [ 401, 403 ])

			# Check no changes were accepted:
			user = User.objects.get(id = self.user_id)
			self.assertNotEqual(user.first_name, 'John')
			self.assertNotEqual(user.father_family_name, 'Doe')
			self.assertEqual(user.photo.name, 'users/default.jpg')

			self.assertTrue(bool(ActionLog.objects.active()))

			log = ActionLog.objects.latest('action_date')
			self.assertEqual(log.category, 1)
			self.assertIn(log.status, [ 401, 403 ])

	def test_view_profile(self):
		"""
			Test which verifies that roles allowed to view other users have access,
			otherwise, that a 40x is replied.
		"""
		action_log_count = ActionLog.objects.active().count()
		response = self.client.get(reverse_lazy('users:view', kwargs = { 'user_id': self.user_id }), follow = True)

		if self.should_pass:
			# If the role has enough privileges, allow
			self.assertEqual(response.status_code, 200)

			# Check if the action log has a new entry:
			self.assertEqual(action_log_count + 1, ActionLog.objects.active().count())

			# Check the entry has the right category and status
			log = ActionLog.objects.latest('action_date')
			self.assertEqual(log.category, 1)
			self.assertEqual(log.status, 200)
		else:
			# Deny
			self.assertIn(response.status_code, [ 401, 403 ])

			# Check if the action log has a new entry:
			self.assertEqual(ActionLog.objects.active().count(), action_log_count + 1)

			# Check the entry has the right category and status
			log = ActionLog.objects.latest('action_date')
			self.assertEqual(log.category, 1)
			self.assertIn(log.status, [401, 403])

	def test_delete_user(self):
		"""
			Test which verifies that roles allowed to delete other users are able to,
			otherwise, that a 40x is replied.
			Main:
				Delete an active user
			Alternatives:
				Delete an inactive user or one that doesn't exist (test_delete_user_invalid)
		"""
		action_log_count = ActionLog.objects.active().count()
		response = self.client.delete(reverse_lazy('users:edit', kwargs = { 'user_id': self.user_id }), follow = True)

		if self.should_pass_delete:
			# If the role has enough privileges, allow
			self.assertEqual(response.status_code, 200)

			# Check if the action log has a new entry:
			self.assertEqual(ActionLog.objects.active().count(), action_log_count + 1)

			# Check the entry has the right category and status
			log = ActionLog.objects.latest('action_date')
			self.assertEqual(log.category, 1)
			self.assertEqual(log.status, 200)
		else:
			# Check the user was not deleted:
			user = User.objects.get(id = self.user_id)
			self.assertTrue(user.active)

	def test_delete_user_invalid(self):
		"""
			Test which verifies that a 40x is replied if the user is invalid or has already been deleted.
		"""
		action_log_count = ActionLog.objects.active().count()
		#Try to delete an invalid user_id
		response = self.client.delete(reverse_lazy('users:edit', kwargs = { 'user_id': 999 }), follow = True)

		# User Manager Only:
		if self.should_pass_delete:
			# Even if the role has enough privileges, deny:
			self.assertIn(response.status_code, [ 401, 403 ])

			# Check if the action log has a new entry:
			self.assertEqual(ActionLog.objects.active().count(), action_log_count + 1)

			# Check the entry has the right category and status
			log = ActionLog.objects.latest('action_date')
			self.assertEqual(log.category, 1)
			self.assertIn(log.status, [401, 403])

class AdminUserTest(_UserTest):
	"""
		Represents the basic data of the user to be tested:
			An admin user basic data
	"""
	email_address = 'test_admin@example.com'
	password = 'ta_asdfg'
	role = Role.objects.get(id = 3)
	should_pass = True
	should_pass_delete = True


class ExternalUserTest(_UserTest):
	"""
		Represents the basic data of the user to be tested:
			A malicious professor account trying to mess with the system privileges basic data >:)
	"""
	email_address = 'test_external@example.com'
	password = 'te_asdfg'
	role = Role.objects.get(id = 2)

class SelfUserTest(_UserTest):
	"""
		Represents the basic data of the user to be tested:
			A professor type account user basic data
	"""
	email_address = 'test@example.com'
	password = 'asdfg'
	role = Role.objects.get(id = 2)
	should_pass = True
	use_self = True

