# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from apps.fmfn.models import (
	ActionLog,
	Material,
	Role,
	Campus,
	Download,
	Language,
	SchoolGrade
)
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
import os

__all__ = [
	'MaterialTest'
]
User = get_user_model()

class MaterialTest(TestCase):
	""" Material CRUD tests:
		- test_material_created: basic material creation flow
		- test_material_edited: basic material edition flow
		- test_material_deleted: basic material deletion flow
		- test_too_much_content: alternative flow where the user inputs both a link and a file
		- test_not_enough_content: alternative flow where the user doesn't input a file nor a link
		- test_material_detail: basic material display flow
		- test_file_uploaded: checks that a file is correctly uploaded to the destination path
	"""

	fixtures = [ 'roles', 'grades', 'campus']

	def setUp(self):

		self.client = Client(enforce_csrf_checks = False)
		self.user = User.objects.create_user(
			email_address = 'test1@example.com',
			password = 'asdfgh',
			role = Role.objects.get(id = 5),
			campus = Campus.objects.get(id = 1)
		)

	def test_material_created(self):
		""" After executing content/create function, verifies that:
			- the http responses are successful
			- the ActionLog contains the latest operation registry
			- the latest entry in the log contains a 200 response code
			- the materials count increased by one
		"""

		material_count = len(Material.objects.active())
		log_count = len(ActionLog.objects.active())

		# Test case: a valid submission arrives
		self.client.login(email_address = 'test1@example.com', password = 'asdfgh')

		response = self.client.post(reverse_lazy('content:create'), data = {
			'title': 'A material test',
			'description': 'This material works best for testing purposes',
			'link':'http://www.google.com'
		}, follow = True)

		# Check the response status sequence
		self.assertEqual(response.status_code, 200)
		url, status = response.redirect_chain[-1]
		self.assertEqual(status, 302)

		# Check the materials count increased by one
		self.assertEqual(len(Material.objects.active()), (material_count + 1))

		# Check the action log
		self.assertTrue(bool(ActionLog.objects.active()))
		self.assertEqual(len(ActionLog.objects.active()), (log_count + 2))
		self.assertEqual(ActionLog.objects.latest('action_date').category, 2)

		self.assertEqual(ActionLog.objects.latest('action_date').status, 200)
	def test_material_edited(self):
		""" After executing edit function, verifies that:
			- the http responses are successful
			- the ActionLog contains the latest operation registry
			- the latest entry in the log contains a 200 response code
			-the fields edited did change in the database
		"""

		self.client.login(email_address = 'test1@example.com', password = 'asdfgh')
		log_count = len(ActionLog.objects.active())

		test_material = Material.objects.create(
								title = 'Material a editar',
								description = 'Descripcion de prueba',
								link = 'http://blah.com'
		)
		test_data = {
			'title': 'Material editado',
			'description': 'Descripción editada',
			'link': 'http://www.hola.com'
		}
		response = self.client.post(reverse_lazy('content:edit', kwargs= {'content_id':test_material.id}), data=test_data, follow=True)
		test_material = Material.objects.active().get(title = 'Material editado')
		# Check the response status sequence
		self.assertEqual(response.status_code, 200)
		url, status = response.redirect_chain[-1]
		self.assertEqual(status, 302)
		# Check the action log
		self.assertTrue(bool(ActionLog.objects.active()))
		self.assertEqual(len(ActionLog.objects.active()), (log_count + 2))
		self.assertEqual(ActionLog.objects.latest('action_date').category, 2)
		self.assertEqual(ActionLog.objects.latest('action_date').status, 200 )
		self.assertEqual(test_data['description'],test_material.description)
		self.assertEqual(test_data['link'],test_material.link)
	def test_material_deleted(self):
		""" After executing delete function, verifies that:
			- the http responses are successful
			- the ActionLog contains the latest operation registry
			- the latest entry in the log contains a 200 response code
			- the active materials count decreased by one
			- the document schema reflects the last operation
		"""

		material = Material.objects.create(
			title = 'Test material',
			description = 'A material destined to test deletion',
			link = 'http://127.0.0.1:8000/',
			user = self.user
		)
		material_count = len(Material.objects.active())
		material_id = material.id

		# Test case: a valid submission arrives
		self.client.login(email_address = 'test1@example.com', password = 'asdfgh')
		response = self.client.delete(reverse_lazy('content:edit', kwargs = { 'content_id': material_id }), follow = True)

		# Check the response status sequence
		self.assertEqual(response.status_code, 200)

		# Test the document schema
		self.assertJSONEqual(str(response.content), {
			'version': '1.0.0',
			'status': 200,
			'material': { 'id': material_id, 'status': 'delete' }
		})

		# Check the materials count increased by one
		self.assertEqual(len(Material.objects.active()), (material_count - 1))

		# Check the action log
		self.assertTrue(bool(ActionLog.objects.active()))
		self.assertEqual(len(ActionLog.objects.active()), 1)
		self.assertEqual(ActionLog.objects.latest('action_date').category, 2)
		self.assertEqual(ActionLog.objects.latest('action_date').status, 200)
	def test_too_much_content(self):
		""" After executing the create function with an invalid set of data (both a file and a link are sent to the function) , verifies that:
			- the http responses are unsuccessful
			- the ActionLog contains the latest operation registry
			- the latest entry in the log contains a 401 response code
			- the object wasn't created
		"""

		self.client.login(email_address = 'test1@example.com', password = 'asdfgh')

		with open('test.txt','w+') as file :
			test_data = {
				'title': 'Material no creado',
				'description': 'Descripción editada',
				'link': 'http://www.hola.com',
				'content': file
			}
			response = self.client.post(reverse_lazy('content:create'),data=test_data)
			# Check the response status sequence
			self.assertEqual(response.status_code, 401)
			# Check the action log
			self.assertTrue(bool(ActionLog.objects.active()))
			self.assertEqual(len(ActionLog.objects.active()), 1)
			self.assertEqual(ActionLog.objects.latest('action_date').category, 2)
			self.assertEqual(ActionLog.objects.latest('action_date').status, 401)
	def test_not_enough_content(self):
		""" After executing the create function with an invalid set of data (neither a file nor a link are sent to the function) , verifies that:
			- the http responses are unsuccessful
			- the ActionLog contains the latest operation registry
			- the latest entry in the log contains a 401 response code
			- the object wasn't modified
		"""

		self.client.login(email_address = 'test1@example.com', password = 'asdfgh')

		response = self.client.post(reverse_lazy('content:create'), data = {
			'title': 'A material test',
			'description': 'This material works best for testing purposes',
		})
		# Check the response status
		self.assertEqual(response.status_code, 401)

		# Check the action log
		self.assertTrue(bool(ActionLog.objects.active()))
		self.assertEqual(len(ActionLog.objects.active()), 1)
		self.assertEqual(ActionLog.objects.latest('action_date').category, 2)
		self.assertEqual(ActionLog.objects.latest('action_date').status, 401 )
	def test_material_detail(self):
		""" After executing the view material function, verifies that:
			- the http responses are successful
			- the ActionLog contains the latest operation registry
			- the latest entry in the log contains a 200 response code
		"""

		self.client.login(email_address = 'test1@example.com', password = 'asdfgh')

		test_material = Material.objects.create(
								title = 'Material a editar',
								description = 'Descripcion de prueba',
								link = 'http://blah.com'
		)
		response = self.client.get(reverse_lazy('content:view',kwargs={'content_id':test_material.id}))
		self.assertEqual(response.status_code,200)
		# Check the action log
		self.assertTrue(bool(ActionLog.objects.active()))
		self.assertEqual(len(ActionLog.objects.active()), 1)
		self.assertEqual(ActionLog.objects.latest('action_date').category, 2)
		self.assertEqual(ActionLog.objects.latest('action_date').status, 200 )
	def test_file_uploaded(self):
		""" After executing the create function, having selected a content file, verifies that:
			- the http responses are successful
			- the ActionLog contains the latest operation registry
			- the latest entry in the log contains a 200 response code
			- the file stored equals the file sent in the form
		"""

		self.client.login(email_address = 'test1@example.com', password = 'asdfgh')
		with open('test.txt','w+') as f:
			f.write(b'testing')

		with open('test.txt','r') as f:
			response = self.client.post(reverse_lazy('content:create'), data = {
				'title': 'file test',
				'description': 'This material works best for testing purposes',
				'content': f
			}, follow = True)

			self.assertEqual(response.status_code, 200)
			saved_file = list(Material.objects.active())[-1].content
			self.assertTrue(cmp(saved_file, file))

		os.remove('test.txt')

	def _create_file(self, add_content = True):

		self.client.login(email_address = 'test1@example.com', password = 'asdfgh')

		with open('media/materials/files/test.jpg','rb') as f:

			data = {
				'title': 'file test',
				'description': 'This material works best for testing purposes'
			}
			if add_content: data['content'] = f
			else: data['link'] = 'http://localhost/'

			self.client.post(reverse_lazy('content:create'), data = data, follow = True)

	def test_no_content(self):

		download_count = len(Download.objects.active())
		log_count = len(ActionLog.objects.active())

		self._create_file(add_content = False)
		self.client.login(email_address = 'test1@example.com', password = 'asdfgh')
		response = self.client.get(reverse_lazy('content:download',kwargs={ 'content_id': Material.objects.last().id }))

		# Check status code
		self.assertEqual(response.status_code, 403)

		# Test action log
		self.assertEqual(len(ActionLog.objects.active()), (log_count + 3))
		self.assertEqual(ActionLog.objects.latest('action_date').category, 2)
		self.assertEqual(ActionLog.objects.latest('action_date').status, 403)

	def test_inactive_material(self):

		download_count = len(Download.objects.active())
		log_count = len(ActionLog.objects.active())

		self._create_file(add_content = False)
		self.client.login(email_address = 'test1@example.com', password = 'asdfgh')

		material = Material.objects.last()
		material.active = False
		material.save()

		response = self.client.get(reverse_lazy('content:download',kwargs = { 'content_id': material.id }), follow = True)

		# Check status code
		self.assertEqual(response.status_code, 403)

		# Test action log
		self.assertEqual(len(ActionLog.objects.active()), (log_count + 3))
		self.assertEqual(ActionLog.objects.latest('action_date').category, 2)
		self.assertEqual(ActionLog.objects.latest('action_date').status, 403)
	def test_material_does_not_exist(self):

		download_count = len(Download.objects.active())
		log_count = len(ActionLog.objects.active())

		response = self.client.get(reverse_lazy('content:download',kwargs = { 'content_id': 0 }), follow = True)

		# Check status code
		self.assertEqual(response.status_code, 403)

		# Check download count
		self.assertEqual(len(Download.objects.active()), download_count)

		# Test action log
		self.assertEqual(len(ActionLog.objects.active()), (log_count + 3))
		self.assertEqual(ActionLog.objects.latest('action_date').category, 2)
		self.assertEqual(ActionLog.objects.latest('action_date').status, 403)

	def test_material_downloaded(self):
		download_count = len(Download.objects.active())
		log_count = len(ActionLog.objects.active())

		self._create_file()
		self.client.login(email_address = 'test1@example.com', password = 'asdfgh')
		response = self.client.get(reverse_lazy('content:download',kwargs = { 'content_id': Material.objects.last().id }), follow = True)

		material = Material.objects.last()

		# Check status code
		self.assertEqual(response.status_code, 200)

		# Check download count
		self.assertEqual(len(Download.objects.active()), (download_count + 1))

		# Test action log
		self.assertEqual(len(ActionLog.objects.active()), (log_count + 3))
		self.assertEqual(ActionLog.objects.latest('action_date').category, 2)
		self.assertEqual(ActionLog.objects.latest('action_date').status, 200)

