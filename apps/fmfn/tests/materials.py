# -*- coding: utf8 -*-
from __future__ import unicode_literals
from apps.fmfn.models import Material
from django.core.urlresolvers import reverse_lazy
from django.test import TestCase, Client
from django.contrib.auth import get_user_model

__all__ = [ 'CreateMaterialsTest' ]
User = get_user_model()

class CreateMaterialsTest(TestCase):

	def setup(self):
		self.client = Client()


	def test_material_created(self):
		response = self.client.post(reverse_lazy('create'), data = {
			'title' : 'Material 1',
			'description' : 'blah blah'
		})
		self.assertEquals(response.status_code,302)
		latest = Material.objects.latest()
		self.assertEquals(latest.id,1)