from django.test import TestCase, Client
from django.core.urlresolvers import reverse_lazy, reverse
from apps.fmfn.models import users
from django.contrib.auth.models import User
from apps.fmfn.models import SchoolGrade

class ProfileTest(TestCase):

	# User Data
	first_name = 'Erick'
	last_name = 'Garcia Garcia'
	email = 'erick.garcia.garcia@gmail.com'
	password = 'test'
	campus = 'QRO Epigmenio'

	SchoolGrade_name = 'Primaria Baja'
	SchoolGrade_min_age = 5
	SchoolGrade_max_age = 8

	SchoolGrade_name_h = 'Primaria Alta'
	SchoolGrade_min_age_h = 9
	SchoolGrade_max_age_h = 12

	def setUp(self):
		"""Tests associated with the "Edit User" view. Both the normal flow and all alternative flows are tested, regarding the
		following scenarios:

			* The user provides valid data for user data visualization
			* The user provides valid data for user creation
			* The user provides valid data for user edition
		"""
		# Configure the test client
		self.client = Client(enforce_csrf_checks = False)

		# Submit the user to be tested
		user = User.objects.create_user(username = self.email, first_name = self.first_name, last_name = self.last_name, email = self.email, password = self.password)
		SchoolGrade_low_primary = SchoolGrade.objects.create( name = self.SchoolGrade_name, min_age = self.SchoolGrade_min_age, max_age = self.SchoolGrade_max_age)
		SchoolGrade_high_primary = SchoolGrade.objects.create( name = self.SchoolGrade_name_h, min_age = self.SchoolGrade_min_age_h, max_age = self.SchoolGrade_max_age_h)
		profile = users.objects.create(user = user, campus = self.campus )
		profile.class_SchoolGrades.add(SchoolGrade_low_primary)
		profile.class_SchoolGrades.add(SchoolGrade_high_primary)


	def test_profiles_are_correctly_obtained(self):
		"""User profiles are retrieved correctly from the system for visualization"""
		response = self.client.get('/users/1')
		self.assertEqual(response.status_code, 200)


	def test_profiles_are_correctly_edited(self):
		""" User profiles are modified correctly on demand
		"""
		user = users.objects.get(user__username=self.email)

		#Submit changes using post:
		new_first_name = 'John'
		new_last_name = 'Albert'
		new_email = 'jalb@mail.com'
		#image and password fields are assumed to work consistently with the framework defined behaviour.s
		new_campus = 'DF'

		self.sendProfileData(new_first_name, new_last_name, new_email, new_campus, 200)

		#Check whether user has been correctly modified

		response = self.client.get('/users/1')
		self.assertEqual(response.status_code, 200)
		user = response.body.user

		self.assertEqual(user.username, self.email)
		self.assertEqual(user.firstname, new_first_name)
		self.assertEqual(user.lastname, new_last_name)
		self.assertEqual(user.email, new_email)

		self.assertEqual(user.campus, new_campus )
		self.assertEqual(user.class_SchoolGrades.get(id=1).name, self.SchoolGrade_name )
		self.assertEqual(user.class_SchoolGrades.get(id=2).name, self.SchoolGrade_name_h )

	def test_profiles_rejected_on_invalid_input(self):
		""" User profiles are rejected for modification on invalid data
		"""
		user = users.objects.get(user__username=self.email)

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

	def sendProfileData(self, first_name, last_name, email, password, campus, status_code):
		response = self.client.post(reverse_lazy('/users/1/edit'), data = {
			'first_name' : first_name,
			'last_name' : last_name,
			'email' : email,
			'campus' : campus,
        })
		self.assertEqual(response.status_code, status_code)


