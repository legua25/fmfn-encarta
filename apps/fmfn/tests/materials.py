# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from apps.fmfn.models import ActionLog, Material, Grade
import json

__all__ = ['CreateMaterialTest', 'EditMaterialTest', 'DeleteMaterialTest']
User = get_user_model()


class CreateMaterialTest(TestCase):
	def setUp(self):
		self.client = Client()
		grade = Grade.objects.create(
			name='Preescolar',
			min_age=3,
			max_age=6
		)
		grade.save()

		# Create test users
		# active user
		user1 = User.objects.create_user(
			username='test1@example.com',
			email='test1@example.com',
			password='asdfg123'
		)
		user1.is_active = True

		# inactive user
		user2 = User.objects.create_user(
			username='test2@example.com',
			email='test2@example.com',
			password='asdfg123'
		)
		user2.is_active = False

		user1.save()
		user2.save()
		ActionLog.objects.all().delete()

	# Checks that the input data was stored successfully in the database
	def test_material_created(self):

		data = {'title': 'Matemáticas I',
		        'description': 'Descripción de material 1',
		        'link': 'http://www.google.com',
		        'suggested_ages': 1,
		        'user': 1};
		response = self.client.post(reverse_lazy('/content/create/'), data)

		# 302 status means the system redirected the user successfully
		self.assertEqual(response.status_code, 302)

		# checking that the latest record's info matches the input

		latest = Material.objects.latest('title')
		self.assertEqual(latest.title, data['title'])
		self.assertEqual(latest.description, data['description'])
		self.assertEqual(latest.link, data['link'])
		self.assertEqual(latest.suggested_ages, data['suggested_ages'])
		self.assertEqual(latest.user, data['description'])

	# Verifies that any inactive is unable to create a material, this test should fail
	# TODO: check that the user has permission to edit a material

	def test_inactive_user(self):
		data = {'title': 'Matemáticas I',
		        'description': 'Descripción de material 1',
		        'link': 'http://www.google.com',
		        'suggested_ages': 1,
		        'user': 2
		        };
		response = self.client.post(reverse_lazy('/content/create'), data)
		# response 401 - unauthorized
		self.assertEqual(response.status_code, 401)


class EditMaterialTest(TestCase):
	def setUp(self):
		self.client = Client()

		# Create test users
		# active user
		user1 = User.objects.create_user(
			username='test1@example.com',
			email='test1@example.com',
			password='asdfg123'
		)
		user1.is_active = True

		material = Material.objects.create(
			title='Actividad de Español II',
			description='Descripción de material español',
			link='http://facebook.com',
			suggested_ages=1,
			user=1
		)

		user1.save()
		material.save()

	def test_material_edited(self):
		data = {'title': 'Matemáticas II',
		        'description': 'Descripción de material 1 edit',
		        'link': 'http://www.google.com.mx',
		        'suggested_ages': 1,
		        'user': 1};
		response = self.client.post(reverse_lazy('/content/1/edit'), data)

		record = Material.objects.latest()
		self.assertEqual(response.status_code, 302)
		self.assertEqual(record.title, data['title'])
		self.assertEqual(record.description, data['description'])
		self.assertEqual(record.link, data['link'])


class DeleteMaterialTest(TestCase):

	def setUp(self):
		self.client = Client()
		material = Material.objects.create(
			title='Actividad de Español II',
			description='Descripción de material español',
			link='http://facebook.com',
			suggested_ages=1,
			user=1
		)
		material.save()

	def test_material_deleted(self):
		response = self.client.delete(reverse_lazy('/content/1/delete'), data={'id': 1})
		self.assertEqual(response.status_code, 302)
		self.assertEqual(Material.objects.get(id=1).is_active, False)

class ListMaterialTest(TestCase):

	def setUp(self):

		self.client = Client()
		Material.objects.create(
			title='Actividad de Español II',
			description='Descripción de material español',
			link='http://facebook.com',
			suggested_ages=1,
			user=1
		)
		Material.objects.create(
			title='Actividad de Matematicas II',
			description='Descripción de material mate',
			link='http://twitter.com',
			suggested_ages=1,
			user=1
		)
		Material.objects.create(
			title='Actividad de Fisica II',
			description='Descripción de material fisica',
			link='http://twitter.com',
			suggested_ages=2,
			user=1
		)

	def test_list_materials(self):
		pass
		# response = self.client.get(reverse_lazy('/content/list'))[:2]
		# response = Material.objects.all()[:2]
		# self.assertEqual(response.status_code, 302)
		# self.assertEqual(Material.objects.all()[:2])

class FilterMaterialTest(TestCase):

	def setUp(self):
		self.client = Client()

		Material.objects.create(
			title='Actividad de Español II',
			description='Descripción de material español',
			link='http://facebook.com',
			suggested_ages=1,
			user=1
		)

		material_2 = Material.objects.create(
			title='Actividad de Matematicas II',
			description='Descripción de material mate',
			link='http://twitter.com',
			suggested_ages=1,
			user=1
		)

		Material.objects.create(
			title='Actividad de Fisica II',
			description='Descripción de material fisica',
			link='http://twitter.com',
			suggested_ages=2,
			user=1
		)

	def filter_materials_test(self):

		Material.objects.create(
			title='Actividad de Español II',
			description='Descripción de material español',
			link='http://facebook.com',
			suggested_ages=1,
			user=1
		)

		Material.objects.create(
			title='Actividad de Matematicas II',
			description='Descripción de material mate',
			link='http://twitter.com',
			suggested_ages=1,
			user=1
		)

		Material.objects.create(
			title='Actividad de Fisica II',
			description='Descripción de material fisica',
			link='http://twitter.com',
			suggested_ages=2,
			user=1
		)

		response = self.client.get(reverse_lazy('content:list'), data = {
			'suggested_ages': '1'
		}, follow = True)

		response_data = json.loads(response.body)
		self.assertTrue(response_data.get('suggested_ages', False))
		resp_data = response_data['data']

		self.assertTrue(bool(Material.objects.active().filter(id__in = [ material['id'] for material in resp_data])))
		self.assertEqual(len(resp_data), len(Material.objects.active()))

		# Test a specific material
		self.assertEqual(response_data['data'][0], {
			'id': 1,
			'name': Material.objects.get(id = 1).name
		})

		# Test response code
		self.assertEqual(response.status_code, 200)


