# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse_lazy
from django.test import TestCase, Client
from apps.fmfn.models import (
	Type,
	Theme,
	Language,
	ActionLog
)
import json

class TagsTest(TestCase):
	""" Defines a generic test for a material tag

		This test is abstract - It is used as a base to define specific test for the types of tags
	"""
	def setUp(self):
		#Create an instance of Client that will receive XML Requests
		self.client = Client(HTTP_X_REQUESTED_WITH='XMLHttpRequest')

	class Meta(object):
		abstract = True

class ThemeTagsTest(TagsTest):
	""" Defines a testing class for Theme type tags

		Tests PUT, POST, GET and DELETE methods for Theme tags
	"""
	def test_put(self):

		# Send request with the desired parameters
		data = { 'type': 'theme', 'name': 'filosofia' }
		response = self.client.put(reverse_lazy('content-tags:create'), data = data, format='json')
		response_data = json.loads(response.body)

		# Test the response returns the correct data
		self.assertEqual(data['type'], response_data['data']['type'])
		self.assertEqual(data['name'], response_data['data']['name'])

		# Test insertion of new tag
		self.assertTrue(bool(Theme.objects.active()))
		self.assertEqual(len(Theme.objects.active()), 1)
		self.assertEqual(Theme.objects.active().get.name, data['name'])

		# Test action log
		self.assertTrue(bool(ActionLog.objects.active()))
		self.assertEqual(len(ActionLog.objects.active()), 1)
		self.assertEqual(ActionLog.objects.latest('action_date').status, 201)
		self.assertEqual(ActionLog.objects.latest('action_date').category, 3)

		# Test response status code
		self.assertEqual(response.status_code, 201)

	def test_post(self):

		# Create object
		Theme.objects.create(name="pedagogia")

		# Send request with the desired parameters
		data = { 'type': 'theme', 'data': {'name': 'filosofia'} }
		response = self.client.post(reverse_lazy('content-tags:edit'), data = data, format='json')
		response_data = json.loads(response.body)

		# Test the response returns the correct data
		self.assertEqual(data['type'], response_data['data']['type'])
		self.assertEqual(data['data']['name'], response_data['data']['name'])

		# Test object is correctly updated
		tag = Theme.objects.get(id = 1)
		self.assertEqual(tag.name, data['data']['name'])

		# Test action log
		self.assertTrue(bool(ActionLog.objects.active()))
		self.assertEqual(len(ActionLog.objects.active()), 1)
		self.assertEqual(ActionLog.objects.latest('action_date').status, 201)
		self.assertEqual(ActionLog.objects.latest('action_date').category, 3)

		# Test response status code
		self.assertEqual(response.status_code, 200)

	def test_get(self):

		# Send request with the desired parameters
		data = {'type': 'theme'}
		response = self.client.get(reverse_lazy('content-tags:list'), data = data, follow = True, format='json')
		response_data = json.loads(response.body)

		# Expect no tags
		self.assertEqual(response_data['status'], 404)

		# Create object in database
		Theme.objects.create(name="filosofia")

		response = self.client.get(reverse_lazy('content-tags:list'), data = data, follow = True, format='json')
		response_data = json.loads(response.body)

		# Test that type is one of the defined tags
		self.assertTrue(response_data.get('type', False) in [ 'type', 'theme', 'language' ])
		# Test that recovered tags exist in Theme tags
		self.assertTrue(bool(Theme.objects.active().filter(id__in = [ tag['id'] for tag in response_data['data']])))
		# Test that the number of tags recovered is the same as the number of existing Theme tags
		self.assertEqual(len(response_data['data']), len(Theme.objects.active()))

		# Test specific tag
		tag = Theme.objects.get(id = 1)
		self.assertEqual(response_data['data'][0]['name'], tag.name)

		# Test action log
		self.assertTrue(bool(ActionLog.objects.active()))
		self.assertEqual(len(ActionLog.objects.active()), 1)
		self.assertEqual(ActionLog.objects.latest('action_date').status, 201)
		self.assertEqual(ActionLog.objects.latest('action_date').category, 3)

		# Test response code
		self.assertEqual(response.status_code, 200)

	def test_delete(self):

		# Create object
		Theme.objects.create(name="pedagogia")

		# Send request with the desired parameters
		data = { 'type': 'theme' }
		response = self.client.delete(reverse_lazy('content-tags:edit'), data = data, format='json')
		response_data = json.load(response.body)

		# Test object is correctly deleted
		tag = Theme.objects.get(id = 1)
		self.assertFalse(tag.active())

		# Test action log
		self.assertTrue(bool(ActionLog.objects.active()))
		self.assertEqual(len(ActionLog.objects.active()), 1)
		self.assertEqual(ActionLog.objects.latest('action_date').status, 201)
		self.assertEqual(ActionLog.objects.latest('action_date').category, 3)

		# Test that the response JSON has status 401
		self.assertEqual(response_data['status', 401])
		# Test that the actual response has status 204
		self.assertEqual(response.status_code, 204)

class TypeTagsTest(TagsTest):
	""" Defines a testing class for Type type tags

		Tests PUT, POST, GET and DELETE methods for Type tags
	"""
	def test_put(self):

		# Send request with the desired parameters
		data = { 'type': 'type', 'name': 'libro' }
		response = self.client.put(reverse_lazy('content-tags:create'), data = data, format='json')
		response_data = json.loads(response.body)

		# Test the response returns the correct data
		self.assertEqual(data['type'], response_data['data']['type'])
		self.assertEqual(data['name'], response_data['data']['name'])

		# Test insertion of new tag
		self.assertTrue(bool(Type.objects.active()))
		self.assertEqual(len(Type.objects.active()), 1)
		self.assertEqual(Type.objects.active().get.name, data['name'])

		# Test action log
		self.assertTrue(bool(ActionLog.objects.active()))
		self.assertEqual(len(ActionLog.objects.active()), 1)
		self.assertEqual(ActionLog.objects.latest('action_date').status, 201)
		self.assertEqual(ActionLog.objects.latest('action_date').category, 3)

		# Test response status code
		self.assertEqual(response.status_code, 201)

	def test_post(self):

		# Create object
		Type.objects.create(name="libro")

		# Send request with the desired parameters
		data = { 'type': 'type', 'data': {'name': 'juego'} }
		response = self.client.post(reverse_lazy('content-tags:edit'), data = data, format='json')
		response_data = json.loads(response.body)

		# Test the response returns the correct data
		self.assertEqual(data['type'], response_data['data']['type'])
		self.assertEqual(data['data']['name'], response_data['data']['name'])

		# Test object is correctly updated
		tag = Type.objects.get(id = 1)
		self.assertEqual(tag.name, data['data']['name'])

		# Test action log
		self.assertTrue(bool(ActionLog.objects.active()))
		self.assertEqual(len(ActionLog.objects.active()), 1)
		self.assertEqual(ActionLog.objects.latest('action_date').status, 201)
		self.assertEqual(ActionLog.objects.latest('action_date').category, 3)

		# Test response status code
		self.assertEqual(response.status_code, 200)

	def test_get(self):

		# Send request with the desired parameters
		data = {'type': 'type'}
		response = self.client.get(reverse_lazy('content-tags:list'), data = data, follow = True, format='json')
		response_data = json.loads(response.body)

		# Expect no tags
		self.assertEqual(response_data['status'], 404)

		# Create object in database
		Type.objects.create(name="libro")

		response = self.client.get(reverse_lazy('content-tags:list'), data = data, follow = True, format='json')
		response_data = json.loads(response.body)

		# Test that type is one of the defined tags
		self.assertTrue(response_data.get('type', False) in [ 'type', 'theme', 'language' ])
		# Test that recovered tags exist in Type tags
		self.assertTrue(bool(Type.objects.active().filter(id__in = [ tag['id'] for tag in response_data['data']])))
		# Test that the number of tags recovered is the same as the number of existing Type tags
		self.assertEqual(len(response_data['data']), len(Type.objects.active()))

		# Test specific tag
		tag = Type.objects.get(id = 1)
		self.assertEqual(response_data['data'][0]['name'], tag.name)

		# Test action log
		self.assertTrue(bool(ActionLog.objects.active()))
		self.assertEqual(len(ActionLog.objects.active()), 1)
		self.assertEqual(ActionLog.objects.latest('action_date').status, 201)
		self.assertEqual(ActionLog.objects.latest('action_date').category, 3)

		# Test response code
		self.assertEqual(response.status_code, 200)

	def test_delete(self):

		# Create object
		Type.objects.create(name="libro")

		# Send request with the desired parameters
		data = { 'type': 'type' }
		response = self.client.delete(reverse_lazy('content-tags:edit'), data = data, format='json')
		response_data = json.load(response.body)

		# Test object is correctly deleted
		tag = Type.objects.get(id = 1)
		self.assertFalse(tag.active())

		# Test action log
		self.assertTrue(bool(ActionLog.objects.active()))
		self.assertEqual(len(ActionLog.objects.active()), 1)
		self.assertEqual(ActionLog.objects.latest('action_date').status, 201)
		self.assertEqual(ActionLog.objects.latest('action_date').category, 3)

		# Test that the response JSON has status 401
		self.assertEqual(response_data['status', 401])
		# Test that the actual response has status 204
		self.assertEqual(response.status_code, 204)

class LanguageTagsTest(TagsTest):
	""" Defines a testing class for Language type tags

		Tests PUT, POST, GET and DELETE methods for Language tags
	"""
	def test_put(self):

		# Send request with the desired parameters
		data = { 'type': 'language', 'name': 'español' }
		response = self.client.put(reverse_lazy('content-tags:create'), data = data, format='json')
		response_data = json.loads(response.body)

		# Test the response returns the correct data
		self.assertEqual(data['type'], response_data['data']['type'])
		self.assertEqual(data['name'], response_data['data']['name'])

		# Test insertion of new tag
		self.assertTrue(bool(Language.objects.active()))
		self.assertEqual(len(Language.objects.active()), 1)
		self.assertEqual(Language.objects.active().get.name, data['name'])

		# Test new tag is the inserted tag
		tag = Language.objects.get(id = 1)
		self.assertEqual(tag.name, data['name'])

		# Test action log
		self.assertTrue(bool(ActionLog.objects.active()))
		self.assertEqual(len(ActionLog.objects.active()), 1)
		self.assertEqual(ActionLog.objects.latest('action_date').status, 201)
		self.assertEqual(ActionLog.objects.latest('action_date').category, 3)

		# Test response status code
		self.assertEqual(response.status_code, 201)

	def test_post(self):

		# Create object
		Type.objects.create(name="español")

		#  Send request with the desired parameters
		data = { 'type': 'language', 'data': {'name': 'español'} }
		response = self.client.post(reverse_lazy('content-tags:edit'), data = data, format='json')
		response_data = json.loads(response.body)

		# Test the response returns the correct data
		self.assertEqual(data['type'], response_data['data']['type'])
		self.assertEqual(data['data']['name'], response_data['data']['name'])

		# Test object is correctly updated
		tag = Language.objects.get(id = 1)
		self.assertEqual(tag.name, data['data']['name'])

		# Test action log
		self.assertTrue(bool(ActionLog.objects.active()))
		self.assertEqual(len(ActionLog.objects.active()), 1)
		self.assertEqual(ActionLog.objects.latest('action_date').status, 201)
		self.assertEqual(ActionLog.objects.latest('action_date').category, 3)

		# Test response status code
		self.assertEqual(response.status_code, 200)

	def test_get(self):

		# Send request with the desired parameters
		data = {'type': 'language'}
		response = self.client.get(reverse_lazy('content-tags:list'), data = data, follow = True, format='json')
		response_data = json.loads(response.body)

		# Expect no tags
		self.assertEqual(response_data['status'], 404)

		# Create object in database
		Type.objects.create(name="libro")

		response = self.client.get(reverse_lazy('content-tags:list'), data = data, follow = True, format='json')
		response_data = json.loads(response.body)

		# Test that type is one of the defined tags
		self.assertTrue(response_data.get('type', False) in [ 'type', 'theme', 'language' ])
		# Test that recovered tags exist in Language tags
		self.assertTrue(bool(Language.objects.active().filter(id__in = [ tag['id'] for tag in response_data['data']])))
		# Test that the number of tags recovered is the same as the number of existing Language tags
		self.assertEqual(len(response_data['data']), len(Language.objects.active()))

		# Test specific tag
		tag = Type.objects.get(id = 1)
		self.assertEqual(response_data['data'][0]['name'], tag.name)

		# Test action log
		self.assertTrue(bool(ActionLog.objects.active()))
		self.assertEqual(len(ActionLog.objects.active()), 1)
		self.assertEqual(ActionLog.objects.latest('action_date').status, 201)
		self.assertEqual(ActionLog.objects.latest('action_date').category, 3)

		# Test response code
		self.assertEqual(response.status_code, 200)


	def test_delete(self):

		# Create object
		Type.objects.create(name="libro")

		# Send request with the desired parameters
		data = { 'type': 'language' }
		response = self.client.delete(reverse_lazy('content-tags:edit'), data = data, format='json')
		response_data = json.load(response.body)

		# Test object is correctly deleted
		tag = Type.objects.get(id = 1)
		self.assertFalse(tag.active())

		# Test action log
		self.assertTrue(bool(ActionLog.objects.active()))
		self.assertEqual(len(ActionLog.objects.active()), 1)
		self.assertEqual(ActionLog.objects.latest('action_date').status, 201)
		self.assertEqual(ActionLog.objects.latest('action_date').category, 3)

		# Test that the response JSON has status 401
		self.assertEqual(response_data['status', 401])
		# Test that the actual response has status 204
		self.assertEqual(response.status_code, 204)



