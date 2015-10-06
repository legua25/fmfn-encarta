# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse_lazy
from django.test import TestCase, Client
from classifiers import Type, Theme, Language, MaterialTag
import json

class TagsTest(TestCase):

	def setUp(self):
		self.client = Client(HTTP_X_REQUESTED_WITH='XMLHttpRequest')

	def test_put(self):
		data = { 'type': 'theme', 'name': 'filosofia' }
		response = self.client.put(reverse_lazy('content-tags:create'), data = data)
		response_json = json.loads(response.body)

		self.assertEqual(data['type'], response_json['data']['type'])
		self.assertEqual(data['name'], response_json['data']['name'])
		self.assertEqual(response.status_code, 201)

	def test_post(self):
		data = { 'type': 'theme', 'data': {'name': 'filosofia'} }

		response = self.client.post(reverse_lazy('content-tags:edit'), data = data)
		response_json = json.loads(response.body)

		self.assertEqual(data['type'], response_json['data']['type'])
		self.assertEqual(data['data']['name'], response_json['data']['name'])
		self.assertEqual(response.status_code, 200)


	def test_get(self):
		responses = []
		Type.objects.create(name = "Humanidades")
		Theme.objects.create(name = "Filosofia")
		Language.objects.create(name = "Español")

		responses[0] = self.client.get(reverse_lazy('content-tags:list'), data = {
			'type': 'language'
		}, follow = True)
		responses[1] = self.client.get(reverse_lazy('content-tags:list'), data = {
			'type': 'type'
		}, follow = True)
		responses[2] = self.client.get(reverse_lazy('content-tags:list'), data = {
			'type': 'theme'
		}, follow = True)

		for response in responses:
			response_data = json.loads(response.body)
			# Test all tags exist in the given category
			self.assertTrue(response_data.get('type', False) in [ 'type', 'theme', 'language' ])
			resp_type = response_data['type']
			resp_data = response_data['data']
			if resp_type == 'type':
				self.assertTrue(bool(Type.objects.active().filter(id__in = [ tag['id'] for tag in resp_data])))
				self.assertEqual(len(resp_data), len(Type.objects.active()))
			elif resp_type == 'theme':
				self.assertTrue(bool(Theme.objects.active().filter(id__in = [ tag['id'] for tag in resp_data])))
				self.assertEqual(len(resp_data), len(Theme.objects.active()))
			elif resp_type == 'language':
				self.assertTrue(bool(Language.objects.active().filter(id__in = [ tag['id'] for tag in resp_data ])))
				self.assertEqual(len(resp_data), len(Language.objects.active()))


		# Test a specific tag
		self.assertEqual(response_data['data'][0], {
			'id': 1,
			'name': Type.objects.get(id = 1).name
		})

		# Test response code
		self.assertEqual(response.status_code, 200)

	def test_delete(self):
		json_string = {'name': 'ingles'}
		json_data = json.dumps(json_string)

		response = self.client.delete(reverse_lazy('content-tags:edit'), json_data, content_type="application/json")


		self.assertEqual(response.status_code, 204)
		self.assertEqual(record.active, False)






