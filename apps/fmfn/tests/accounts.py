# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from apps.fmfn.models import ActionLog

__all__ = [
	'LoginTest',
	'LogoutTest'
]

User = get_user_model()
class LoginTest(TestCase):
	""" Tests associated with the "login" view. Both the normal flow and all alternative flows are tested, regarding the
		following scenarios:

			* The user provides an invalid set of credentials
			* The user provides a partially invalid set of credentials
			* The user provides credentials for an account which was deactivated by the system administration
			* The user provides valid credentials for an active user
			* The user attempts to log in again with a valid session in use
	"""

	def setUp(self):

		# Configure the test client
		self.client = Client(enforce_csrf_checks = False)

		# Create test users
		User.objects.create_user(
			username = 'test1@example.com',
			email = 'test1@example.com',
			password = 'asdfg123'
		)

		user = User.objects.create_user(
			username = 'test2@example.com',
			email = 'test2@example.com',
			password = 'asdfg123'
		)
		user.is_active = False
		user.save()

		# Clear the action log
		ActionLog.objects.all().delete()

	def test_invalid_user(self):
		""" Verifies the login view with invalid user credentials. In this alternative flow, the user is not validated,
			the action is logged under the "account control" category and the user form is updated to show the credential
			error.
		"""

		# Test case: the user does not exist in the database
		response = self.client.post(reverse_lazy('accounts:login'), data = {
            'email_address': 'test3@example.com',
			'password': 'asdfg123'
        })

		# The user should not have been logged in - authentication failed (HTTP 401)
		self.assertEqual(response.status_code, 401)

		# The action should have been logged - check the action category (account control) and status code (401)
		self.assertEqual(len(ActionLog.objects.all()), 1)
		self.assertEqual(ActionLog.objects.latest('action_date').category, 1)
		self.assertEqual(ActionLog.objects.latest('action_date').status, 401)
	def test_mismatched_password(self):
		""" Verifies the login view with a mismatched set of user credentials in which the email corresponds to a valid
			user but the password does not. In this alternative flow, the user will not be validated and the action will
			be logged under the "account control" category. The form is updated to reflect the errors.
		"""

		# Test case: email address is valid, but password isn't
		response = self.client.post(reverse_lazy('accounts:login'), data = {
            'email_address': 'test1@example.com',
			'password': 'asdfgh123'
        })

		# The user should not have been logged in - authentication failed (HTTP 401)
		self.assertEqual(response.status_code, 401)

		# The action should have been logged - check the action category (account control) and status code (401)
		self.assertEqual(len(ActionLog.objects.all()), 1)
		self.assertEqual(ActionLog.objects.latest('action_date').category, 1)
		self.assertEqual(ActionLog.objects.latest('action_date').status, 401)
	def test_inactive_user(self):
		""" Verifies the login view with a valid user account which has been deactivated by the system administrators.
			In this alternative flow, the user is authenticated but is not validated due to inactivity. The error
			is logged into the "account control" category and the form is updated with the error notifications.
		"""

		# Test case: credentials are valid, but user is not longer active
		response = self.client.post(reverse_lazy('accounts:login'), data = {
            'email_address': 'test2@example.com',
			'password': 'asdfg123'
        })

		# The user should not have been logged in - authentication failed (HTTP 401)
		self.assertEqual(response.status_code, 401)

		# The action should have been logged - check the action category (account control) and status code (401)
		self.assertEqual(len(ActionLog.objects.all()), 1)
		self.assertEqual(ActionLog.objects.latest('action_date').category, 1)
		self.assertEqual(ActionLog.objects.latest('action_date').status, 401)
	def test_active_user(self):
		""" Verifies the login view with a valid, active user account. This normal flow case should authenticate the
			user, deem him/her as valid and log them in, redirecting them afterwards. This action is logged into the
			database under the "account control" category before the redirection.
		"""

		# Test case: credentials are valid and user can be logged in
		response = self.client.post(reverse_lazy('accounts:login'), data = {
            'email_address': 'test1@example.com',
			'password': 'asdfg123'
        }, follow = True)

		# The user should have been logged in - authentication succeeded (HTTP 200)
		self.assertEqual(response.status_code, 200)

		# The action should have been logged - check the action category (account control) and status code (200)
		self.assertEqual(len(ActionLog.objects.all()), 1)
		self.assertEqual(ActionLog.objects.latest('action_date').category, 1)
		self.assertEqual(ActionLog.objects.latest('action_date').status, 200)

		# The user is, indeed, the test user #1
		user = response.wsgi_request.user
		self.assertEqual(user.email, 'test1@example.com')
		self.assertEqual(user.id, 1)
	def test_already_logged_in(self):
		""" Verifies the login view with an already authenticated user. This alternative flow should immediately redirect
			the user to the main site. The redirection is logged under the "account control" category.
		"""

		# Test case: the logged in user can access the restricted "search" view
		result = self.client.login(username = 'test1@example.com', password = 'asdfg123')
		self.assertTrue(result)

		response = self.client.get(reverse_lazy('accounts:login'), follow = True)
		self.assertEqual(response.status_code, 200)

		# The action should have been logged - check the action category (account control) and status code (200)
		self.assertEqual(len(ActionLog.objects.all()), 1)
		self.assertEqual(ActionLog.objects.latest('action_date').category, 1)
		self.assertEqual(ActionLog.objects.latest('action_date').status, 302)

class LogoutTest(TestCase):
	""" Tests associated with the "logout" view. Only the normal flow is tested since the alternate flows are handled by
		the framework, which is already validated.
	"""

	def setUp(self):

		# Configure the test client
		self.client = Client(enforce_csrf_checks = False)

		# Create test users
		User.objects.create_user(
			username = 'test1@example.com',
			email = 'test1@example.com',
			password = 'asdfg123'
		)

		# Clear the action log
		ActionLog.objects.all().delete()

	def test_logout_user(self):
		""" Verifies the logout view with a valid, authenticated user. As part of the normal flow, the action is logged
			into the database under the "account control" category, and the user is logged out. Immediately after, the
			user is redirected to the main site, which in turn redirects him/her to the login page.
		"""

		# Test case: a user logs out from the site
		result = self.client.login(username = 'test1@example.com', email = 'test1@example.com', password = 'asdfg123')
		self.assertTrue(result)

		# Log the user out, then test aftermath
		response = self.client.get(reverse_lazy('accounts:logout'), follow = True)

		# Check the URL and the redirection status
		url, status = response.redirect_chain[-1]
		self.assertEqual(status, 302)
		self.assertTrue(url.endswith(reverse('accounts:login')))

		# Test the log creation
		self.assertEqual(len(ActionLog.objects.all()), 1)
		self.assertEqual(ActionLog.objects.latest('action_date').category, 1)
		self.assertEqual(ActionLog.objects.latest('action_date').status, 200)
