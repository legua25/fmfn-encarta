# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from apps.fmfn.models import (
	ActionLog,
	Material,
	Comment,
	Role,
	Campus
)
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.test import TestCase, Client

__all__ = [
	'RatingsTest'
]
User = get_user_model()

class RatingsTest(TestCase):
	"""
	Tests for the Comment/Rate Material use cases.
	"""

	fixtures = [ 'roles', 'grades', 'campus','materials']

	def setUp(self):

		self.client = Client(enforce_csrf_checks = False, HTTP_X_REQUESTED_WITH = 'XMLHttpRequest')
		self.user = User.objects.create_user(
			email_address = 'test1@example.com',
			password = 'asdfgh',
			role = Role.objects.get(id = 2),
			campus = Campus.objects.get(id = 1)
		)
		self.material = Material.objects.create(
			title = 'Test',
			description = 'test description',
			link = 'http://localhost/',
			user = User.objects.create_user(
				email_address = 'test2@example.com',
				password = 'asdfgh',
				role = Role.objects.get(id = 4),
				campus = Campus.objects.get(id = 1)
			)
		)

	def test_comment_material(self):
		"""
		When a comment and a rating is added to a material, this test verifies:
		 - the response status code is 200 (OK)
		 - the comment count increased by one
		 - the comment is registered correctly in the database
		 - a rating is assigned along with the comment
		 - the comment's length is not greater than 500
		 - the comment is not empty
		 - the user who published the comment appears as the comment's author
		 - the ActionLog contains the latest operation registry
		 - the latest entry in the log contains a 200 response code
		"""

		self.client.login(email_address = 'test1@example.com', password = 'asdfgh')
		comment_count = len(Comment.objects.active())
		log_count = len(ActionLog.objects.active())

		response = self.client.post(reverse_lazy('content:view',kwargs={'content_id':self.material.id}),data = {'content':'Test comment','rating_value':4 })

		self.assertEqual(response.status_code, 201)
		self.assertEqual(len(Comment.objects.active()), comment_count + 1)

		comment = Comment.objects.get(id = 1)
		self.assertEqual(comment.content,'Test comment')
		self.assertEqual(comment.user,self.user)

		self.assertJSONEqual(str(response.content), {
			'version': '1.0.0',
			'status': 201,
			'data': {
				'content': comment.content,
				'user': self.user.id,
				'material': self.material.id,
				'rating': comment.rating_value
			}
		})

		self.assertEqual(len(ActionLog.objects.active()), (log_count + 1))
		self.assertEqual(ActionLog.objects.latest('action_date').category, 2)
		self.assertEqual(ActionLog.objects.latest('action_date').status, 201)

	def test_comment_no_rating(self):
		"""
		When a comment and a rating is added to a material and a rating hasn't been , this test verifies:
		 - the response status code is 400 (Bad Request)
		 - the comment count did not increase
		 - the ActionLog contains the latest operation registry
		 - the latest entry in the log contains a 403 response code
		"""

		self.client.login(email_address = 'test1@example.com', password = 'asdfgh')
		comment_count = len(Comment.objects.active())
		log_count = len(ActionLog.objects.active())
		response = self.client.post(reverse_lazy('content:view',kwargs={'content_id':self.material.id}),data = {'user':self.user, 'content':'Test comment'})
		self.assertEqual(response.status_code,403)
		self.assertEqual(comment_count,0)
		self.assertTrue(bool(ActionLog.objects.active()))
		self.assertEqual(len(ActionLog.objects.active()), (log_count + 1))
		self.assertEqual(ActionLog.objects.latest('action_date').category, 2)
		self.assertEqual(ActionLog.objects.latest('action_date').status, 403)

	def test_comment_twice(self):
		"""
		When a user attempts to add a comment and a rating to a material he/she has previously reviewed, this test verifies:
		 - the response status code is 400 (Bad Request)
		 - the comment count did not increase
		 - the ActionLog contains the latest operation registry
		 - the latest entry in the log contains a 403 response code
		"""

		self.client.login(email_address = 'test1@example.com', password = 'asdfgh')
		comment_count = len(Comment.objects.active())
		log_count = len(ActionLog.objects.active())
		Comment.objects.create(content='This comment will not be posted',rating_value=3,material=self.material,user=self.user)
		response = self.client.post(reverse_lazy('content:view',kwargs={'content_id':self.material.id}),data = {'content':'Test comment','rating_value':4 })
		self.assertEqual(response.status_code,403)
		self.assertEqual(comment_count,0)
		self.assertTrue(bool(ActionLog.objects.active()))
		self.assertEqual(len(ActionLog.objects.active()), (log_count + 1))
		self.assertEqual(ActionLog.objects.latest('action_date').category, 2)
		self.assertEqual(ActionLog.objects.latest('action_date').status, 403)

