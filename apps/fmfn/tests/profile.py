from django.test import TestCase
from apps.fmfn.models import Profile
from django.contrib.auth.models import User

class ProfileTestCase(TestCase):

	first_name = 'Erick'
	last_name = 'Garcia Garcia'
	email = 'erick.garcia.garcia@gmail.com'
	password = 'test'

	def setUp(self):
		# Right data submitted
		user = User.objects.create_user(username = self.email, first_name = self.first_name, last_name = self.last_name, email = self.email, password = self.password)
		Profile.objects.create(user = user)

	def test_profiles_are_correctly_created(self):
		"""user profiles are correctly created and stored data is consistent with the one provided beforehand"""
		user = Profile.objects.get(user__username=self.email)
		self.assertEqual(user.username, self.email)
		self.assertEqual(user.firstname, self.first_name)
		self.assertEqual(user.lastname, self.last_name)
		self.assertEqual(user.email, self.email)
