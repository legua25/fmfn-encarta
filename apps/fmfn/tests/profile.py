from django.test import TestCase, Client
from django.core.urlresolvers import reverse_lazy, reverse
from apps.fmfn.models import Profile
from django.contrib.auth.models import User
from apps.fmfn.models import Grade

class ProfileTest(TestCase):



	# User Data
	first_name = 'Erick'
	last_name = 'Garcia Garcia'
	email = 'erick.garcia.garcia@gmail.com'
	password = 'test'
	campus = 'QRO Epigmenio'

	grade_name = 'Primaria Baja'
	grade_min_age = 5
	grade_max_age = 8

	grade_name_h = 'Primaria Alta'
	grade_min_age_h = 9
	grade_max_age_h = 12

	def setUp(self):
		"""Tests associated with the "Edit User" view. Both the normal flow and all alternative flows are tested, regarding the
		following scenarios:

			* The user provides valid data for user data visualization
			* The user provides valid data for user creation
			* The user provides valid data for user edition
		"""
		# Configure the test client
		self.client = Client(enforce_csrf_checks = False)

		# Right data submitted
		user = User.objects.create_user(username = self.email, first_name = self.first_name, last_name = self.last_name, email = self.email, password = self.password)
		grade_low_primary = Grade.objects.create( name = self.grade_name, min_age = self.grade_min_age, max_age = self.grade_max_age)
		grade_high_primary = Grade.objects.create( name = self.grade_name_h, min_age = self.grade_min_age_h, max_age = self.grade_max_age_h)
		profile = Profile.objects.create(user = user, campus = self.campus )
		profile.class_grades.add(grade_low_primary)
		profile.class_grades.add(grade_high_primary)

	def test_profiles_are_correctly_created(self):
		"""user profiles are correctly created and stored data is consistent with the one provided beforehand"""
		user = Profile.objects.get(user__username=self.email)
		self.assertEqual(user.username, self.email)
		self.assertEqual(user.firstname, self.first_name)
		self.assertEqual(user.lastname, self.last_name)
		self.assertEqual(user.email, self.email)

		self.assertEqual(user.campus, self.campus)
		self.assertEqual(user.class_grades.get(id=1).name, self.grade_name )
		self.assertEqual(user.class_grades.get(id=2).name, self.grade_name_h )

	def test_profiles_are_correctly_obtained(self):
		"""User profiles are retrieved correctly from the system for visualization"""
		response = self.client.get('/users/1')
		self.assertEqual(response.status_code, 200)


	def test_profiles_are_correctly_edited(self):
		""" User profiles are modified correctly on demand
			------------  Work in progress --------- Work in progress -------------
		"""
		# TODO: Assess if this is more or less the way to correctly test this module.

		#Submit changes using post:

		response = self.client.post(reverse_lazy('/users/1/edit'), data = {
			'first_name' : self.first_name,
			'last_name' : self.last_name,
			'email' :self.email,
			'password' : 'test_password_2',
			'campus' : self.campus,
        })

		#Check whether user has been correctly modified