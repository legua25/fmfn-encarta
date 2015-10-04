# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.urlresolvers import reverse_lazy
from django.test import TestCase, Client
from classifiers import Type, MaterialTag
import json

class TagsTest(TestCase):

	def setUp(self):
		self.client = Client()

	def test_put(self):
		json_string = {'name': 'ingles'}
		json_data = json.dumps(json_string)

		response = self.client.put(reverse_lazy('content-tags:create'), json_data, content_type="application/json")

		self.assertEqual(json_data['name'], response.data['name'])
		self.assertEqual(response.status_code, 201)

	def test_post(self):
		json_string = {'name': 'frances'}
		json_data = json.dumps(json_string)

		response = self.client.post(reverse_lazy('content-tags:edit'), json_data, content_type="application/json")
		record = MaterialTag.objects.latest()

		self.assertEqual(response.status_code, 302)
		self.assertEqual(record.name, json_string['name'])


	def test_get(self):
		self.tag = Type(name="ingles")
		self.tag.save()

		response = self.client.get(reverse_lazy('content-tags:list'), HTTP_X_REQUESTED_WITH='XMLHttpRequest')
		json_data = response.content
		json_string = json.loads(json_data)
		expected_schema = {"name": "ingles"}

		self.assertEqual(json_string, expected_schema)
		self.assertEqual(response.status_code, 200)

	def test_delete(self):
		json_string = {'name': 'ingles'}
		json_data = json.dumps(json_string)

		response = self.client.delete(reverse_lazy('content-tags:edit'), json_data, content_type="application/json")
		record = MaterialTag.objects.latest()

		self.assertEqual(response.status_code, 204)
		self.assertEqual(record.active, False)






