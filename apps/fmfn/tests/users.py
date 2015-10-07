from django.test import TestCase, Client
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from apps.fmfn.models import SchoolGrade
from apps.fmfn.models import Campus
from apps.fmfn.models import Role
from apps.fmfn.models import ActionLog

User = get_user_model()

class UsersTest(TestCase):

	# Admin User Data
	first_name_admin = 'Erick'
	last_name_father_admin = 'Garcia'
	last_name_mother_admin = 'Garcia'
	email_admin = 'erick.garcia.garcia@gmail.com'
	password_admin = 'test_9s92hs'

	# Self Professor User Data
	first_name = 'Daniel'
	last_name_father = 'Blanco'
	last_name_mother = 'Castillo'
	email = 'daniel.blanco.castillo@gmail.com'
	password = 'test_jk1ls'

	# Other Professor User Data
	first_name_other = 'Pepe'
	last_name_father_other = 'Troll'
	last_name_mother_other = 'Del Campo'
	email_other = 'ptdco@gmail.com'
	password_other = 'test_kswmc'

	fixtures = [
		'grades',
		'campus',
		'roles'
	]

	def setUp(self):
		"""Tests associated with the "Edit User" view. Both the normal flow and all alternative flows are tested, regarding the
		following scenarios:

			Edit:
				* The admin posts user data changes
				* The professor posts data changes to its own account
				* Other professor posts data changes to other account
			Delete:
				* The admin deletes a user
				* The professor tries to delete its own account
				* Other professor tries to delete other account
		"""
		# Configure the test client
		self.client = Client(enforce_csrf_checks = False)

		# Create the user required for the tests

		self.user = User.objects.create_user(
		 	email_address = self.email,
		 	password = self.password,
		 	first_name = self.first_name,
		 	father_family_name = self.last_name_father,
			mother_family_name = self.last_name_mother,
			grades = SchoolGrade.objects.active().filter(id__in = [ 1, 2 ]),
			campus = Campus.objects.active().filter(id = 1),
			role = Role.objects.active().filter(id = 3)
		 )

		self.user_admin = User.objects.create_user(
		 	email_address = self.email_admin,
		 	password = self.password_admin,
		 	first_name = self.first_name_admin,
		 	father_family_name = self.last_name_father_admin,
			mother_family_name = self.last_name_mother_admin,
			grades = SchoolGrade.objects.active().filter(id__in = [ 1, 2 ]),
			campus = Campus.objects.active().filter(id = 1),
			role = Role.objects.active().filter(id = 1)
		 )

		self.user_other = User.objects.create_user(
		 	email_address = self.email_other,
		 	password = self.password_other,
		 	first_name = self.first_name_other,
		 	father_family_name = self.last_name_father_other,
			mother_family_name = self.last_name_mother_other,
			grades = SchoolGrade.objects.active().filter(id__in = [ 1, 2 ]),
			campus = Campus.objects.active().filter(id = 1),
			role = Role.objects.active().filter(id = 3)
		 )

	def test_profiles_are_correctly_edited_admin(self):
		""" User profiles are modified correctly on demand if role is account manager or above"""

		self.client.login(credentials = {
            'email_address': self.user_admin.email_address,
			'password': self.user_admin.password
        })

		#Submit changes using post:
		new_first_name = 'John'
		new_last_name = 'Albert'
		new_email = 'jalb@mail.com'


		response = self.client.post(reverse_lazy('users:edit', kwargs = { 'user_id': self.user.id }), data = {
			'first_name' : new_first_name,
			'last_name' : new_last_name,
			'email' : new_email,
        })
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.redirect_chain[-1], 302)

		self.user.refresh_from_db()

		#Check whether user has been correctly modified

		self.assertEqual(self.user.first_name, new_first_name)
		self.assertEqual(self.user.lastname, new_last_name)
		self.assertEqual(self.user.email_address, new_email)

		# The action should have been logged - check the action category (account control) and status code (401)

		self.assertEqual(ActionLog.objects.latest('action_date').category, 1)
		self.assertEqual(ActionLog.objects.latest('action_date').status, 200)

	def test_profiles_are_rejected_if_other_edited(self):
		""" User profiles are modified correctly on demand if role is account manager or above"""

		self.client.login(credentials = {
            'email_address': self.user_other.email_address,
			'password': self.user_other.password
        })

		#Submit changes using post:
		new_first_name = 'John'
		new_last_name = 'Albert'
		new_email = 'jalb@mail.com'


		response = self.client.post(reverse_lazy('users:edit', kwargs = { 'user_id': self.user.id }), data = {
			'first_name' : new_first_name,
			'last_name' : new_last_name,
			'email' : new_email,
        })

		self.assertEqual(response.status_code, 401)
		self.assertEqual(response.redirect_chain[-1], 302)

		self.user.refresh_from_db()

		#Check whether user has been correctly modified

		self.assertEqual(self.user.first_name, new_first_name)
		self.assertEqual(self.user.lastname, new_last_name)
		self.assertEqual(self.user.email_address, new_email)

		# The action should have been logged - check the action category (account control) and status code (401)

		self.assertEqual(ActionLog.objects.latest('action_date').category, 1)
		self.assertEqual(ActionLog.objects.latest('action_date').status, 401)

	def test_profiles_rejected_on_invalid_input(self):
		""" User profiles are rejected for modification on invalid data	"""
		user = User.objects.get(user__username=self.email)

		# Submit wrong input changes using post:
		# 30 char limit
		new_first_name = 'JohnJohnJohnJohnJohnJohnJohnJohnJohnJohnJohn'
		new_last_name = 'AlbertAlbertAlbertAlbertAlbertAlbert'
		new_email = 'jalbmail.com'
		new_email2 = 'jalb@mailcom'
		new_email3 = 'jalb@@mail.com'
		#image and password fields are assumed to work consistently with the framework defined behaviour.
		new_campus = 'DFDFDFDFDFDFDFDFDFDFDFDFDFDFDFDFDFDFDFDFDFDFDFDFDFDFDFDFDFDFDFDFDF'

		# Test sending invalid first_name: 30+ char's
		self.sendProfileData(new_first_name, self.last_name, self.email, self.password, self.campus, 400)

		# Test sending invalid last_name: 30+ char's
		self.sendProfileData(self.first_name, new_last_name, self.email, self.password, self.campus, 400)

		# Test sending invalid email: without "@"
		self.sendProfileData(self.first_name, self.last_name, new_email, self.password, self.campus, 400)

		# Test sending invalid email: without "."
		self.sendProfileData(self.first_name, self.last_name, new_email2, self.password, self.campus, 400)

		# Test sending invalid email: with "@@"
		self.sendProfileData(self.first_name, self.last_name, new_email3, self.password, self.campus, 400)

		# Test sending invalid campus: 64+ char's
		self.sendProfileData(self.first_name, self.last_name, self.email, self.password, new_campus, 400)

		#Check whether user has not been modified

		response = self.client.get('/users/1')
		self.assertEqual(response.status_code, 200)
		user = response.body.user

		self.assertEqual(user.username, self.email)
		self.assertEqual(user.firstname, self.first_name)
		self.assertEqual(user.lastname, self.last_name)
		self.assertEqual(user.email, self.email)

		self.assertEqual(user.campus, self.campus )
		self.assertEqual(user.class_SchoolGrades.get(id=1).name, self.SchoolGrade_name )
		self.assertEqual(user.class_SchoolGrades.get(id=2).name, self.SchoolGrade_name_h )

	def sendProfileData(self, first_name, last_name, email, campus, status_code):
		response = self.client.post(reverse_lazy('users:edit', kwargs = { 'user_id': self.user.id }), data = {
			'first_name' : first_name,
			'last_name' : last_name,
			'email' : email,
			'campus' : campus,
        })
		self.assertEqual(response.status_code, status_code)


