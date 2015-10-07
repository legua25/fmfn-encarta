# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.tokens import default_token_generator as tokens
from django.utils.http import urlsafe_base64_encode as b64, force_str
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from apps.fmfn.models import ActionLog

__all__ = [
	'LoginTest',
	'LogoutTest',
	'RecoveryTest'
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
			email_address = 'test1@example.com',
			password = 'asdfg123'
		)
		User.objects.create_user(
			email_address = 'test2@example.com',
			password = 'asdfg123',
			active = False
		)

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
		self.assertEqual(user.email_address, 'test1@example.com')
	def test_already_logged_in(self):
		""" Verifies the login view with an already authenticated user. This alternative flow should immediately redirect
			the user to the main site. The redirection is logged under the "account control" category.
		"""

		# Test case: the logged in user can access the restricted "search" view
		result = self.client.login(email_address = 'test1@example.com', password = 'asdfg123')
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
			email_address = 'test1@example.com',
			password = 'asdfg123'
		)

	def test_logout_user(self):
		""" Verifies the logout view with a valid, authenticated user. As part of the normal flow, the action is logged
			into the database under the "account control" category, and the user is logged out. Immediately after, the
			user is redirected to the main site, which in turn redirects him/her to the login page.
		"""

		# Test case: a user logs out from the site
		result = self.client.login(email_address = 'test1@example.com', password = 'asdfg123')
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
class RecoveryTest(TestCase):
	""" Tests associated with the "recover" view, in its dual modes: "recover" and "reset". Both the normal
		flow and all alternative flows are tested, regarding the following scenarios:

			* The user provides an invalid email address
			* The user is attempting to recover an already logged in account
			* The user tampers the reset form parameters purposely
			* The user provides a password and mismatches the confirmation
			* The user provides a password which matches the user's current password
			* The user provides a totally new password for the user account
	"""

	def setUp(self):

		# Configure the test client
		self.client = Client(enforce_csrf_checks = False)

		# Create test users
		self.user = User.objects.create_user(
			email_address = 'test1@example.com',
			password = 'asdfg123'
		)

	def test_already_logged_in(self):
		""" Verifies the recovery view with an already authenticated user. This alternative flow should redirect the user
			immediately, since it makes no sense to be able to recover the password of a logged in user: to log in, they
			surely remember the password (this is an obvious statement, but nevertheless asserted as true).
		"""

		# Test case: the user is already logged in
		result = self.client.login(email_address = 'test1@example.com', password = 'asdfg123')
		self.assertTrue(result)

		response = self.client.get(reverse_lazy('accounts:recover'), follow = True)
		self.assertEqual(response.status_code, 200)

		# The user should have been redirected and the action should have been logged - check the action log (account control) and status code (302)
		self.assertEqual(len(ActionLog.objects.all()), 1)
		self.assertEqual(ActionLog.objects.latest('action_date').category, 1)
		self.assertEqual(ActionLog.objects.latest('action_date').status, 302)
	def test_mismatched_email(self):
		""" Verifies the recovery view ("recover" mode) with an email address which is not registered in the database. In this
			alternate scenario, the request fails and the action is logged.
		"""

		# Test case: attempting to recover an invalid account
		response = self.client.post(reverse_lazy('accounts:recover'), data = {
			'email_address': 'test2@example.com'
		}, follow = True)

		# The user does not exist - the operation has failed (HTTP 401)
		self.assertEqual(response.status_code, 401)

		# The action should have been logged - check the action category (account control) and status code (401)
		self.assertEqual(len(ActionLog.objects.all()), 1)
		self.assertEqual(ActionLog.objects.latest('action_date').category, 1)
		self.assertEqual(ActionLog.objects.latest('action_date').status, 401)
	def test_tampered_GET(self):
		""" Verifies the recovery view ("reset" mode) with a purposely altered request in order to edit another user.
			This alternate path may lead to a security breach, therefore the attempt is immediately blocked and forbidden
			further access into the system.
		"""

		# Test case: invalid but possibly valid user data is used instead of the expected user
		u = User(email_address = 'test2@example.com')
		u.set_password('asdfg123')
		u.id = 3

		response = self.client.get(reverse_lazy('accounts:reset', kwargs = {
			'user_id': b64(force_str(u.id)),
			'token': tokens.make_token(u)
		}),
		follow = True)

		# The request must have failed abruptly - the action should have been logged and a HTTP 403 Forbidden should have been returned
		self.assertEqual(response.status_code, 403)
		self.assertEqual(len(ActionLog.objects.all()), 1)
		self.assertEqual(ActionLog.objects.latest('action_date').category, 1)
		self.assertEqual(ActionLog.objects.latest('action_date').status, 403)
	def test_tampered_POST(self):
		""" Verifies the recovery view ("reset" mode) with a purposely altered request in order to edit another user.
			This alternate path may lead to a security breach, therefore the attempt is immediately blocked and forbidden
			further access into the system.
		"""

		# Test case: invalid but possibly valid user data is used instead of the expected user
		u = User(email_address = 'test2@example.com')
		u.set_password('asdfg123')
		u.id = 3

		response = self.client.post(reverse_lazy('accounts:reset', kwargs = {
			'user_id': b64(force_str(u.id)),
			'token': tokens.make_token(u)
		}),
		follow = True)

		# The request must have failed abruptly - the action should have been logged and a HTTP 403 Forbidden should have been returned
		self.assertEqual(response.status_code, 403)
		self.assertEqual(len(ActionLog.objects.all()), 1)
		self.assertEqual(ActionLog.objects.latest('action_date').category, 1)
		self.assertEqual(ActionLog.objects.latest('action_date').status, 403)
	def test_wrong_passwords(self):
		""" Verifies the recovery view ("reset" mode) with a request in which the confirmation password
			does not match the provided password. In this alternate path, the request cannot be completed and
			the action is logged.
		"""

		# Test case: the user provides the very same password as a replacement for his current one
		url_params = { 'user_id': b64(force_str(self.user.id)), 'token': tokens.make_token(self.user) }
		response = self.client.post(reverse_lazy('accounts:reset', kwargs = url_params), data = {
			'password': 'asdfgh123',
			'repeat': 'asdfgh124'
		}, follow = True)

		# The password is not changed - the action is logged and the response is an unauthorized action (401)
		self.assertEqual(response.status_code, 401)
		self.assertEqual(len(ActionLog.objects.all()), 1)
		self.assertEqual(ActionLog.objects.latest('action_date').category, 1)
		self.assertEqual(ActionLog.objects.latest('action_date').status, 401)
	def test_same_password(self):
		""" Verifies the recovery view ("reset" mode) with a request in which the confirmation password
			matches the given password, but this one matches the current user password. In this alternate
			path, the request cannot be completed and the action is logged.
		"""

		# Test case: the user provides the very same password as a replacement for his current one
		url_params = { 'user_id': b64(force_str(self.user.id)), 'token': tokens.make_token(self.user) }
		response = self.client.post(reverse_lazy('accounts:reset', kwargs = url_params), data = {
			'password': 'asdfg123',
			'repeat': 'asdfg123'
		}, follow = True)

		# The action should have been logged - check the action category (account control) and status code (401)
		self.assertEqual(response.status_code, 401)
		self.assertEqual(len(ActionLog.objects.all()), 1)
		self.assertEqual(ActionLog.objects.latest('action_date').category, 1)
		self.assertEqual(ActionLog.objects.latest('action_date').status, 401)
	def test_new_password(self):
		""" Verifies the recovery view ("reset" mode) with a request in which the confirmation password
			matches the given password and the password is different form the current one. In this scenario,
			the user's password is changed and the action is logged.
		"""

		# Test case: the user provides a new password, which can be replaced
		url_params = { 'user_id': b64(force_str(self.user.id)), 'token': tokens.make_token(self.user) }
		response = self.client.post(reverse_lazy('accounts:reset', kwargs = url_params), data = {
			'password': 'asdfgh123',
			'repeat': 'asdfgh123'
		}, follow = True)

		# The action should have been logged - check the action category (account control) and status code (200)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(len(ActionLog.objects.all()), 1)
		self.assertEqual(ActionLog.objects.latest('action_date').category, 1)
		self.assertEqual(ActionLog.objects.latest('action_date').status, 200)

		# The user's password changed - test this
		self.user.refresh_from_db()
		self.assertTrue(self.user.check_password('asdfgh123'))
