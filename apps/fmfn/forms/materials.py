# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from apps.fmfn.models import Material, Theme, Type, Language
from django.forms import *
from django.forms import ModelForm as Form

__all__ = [ 'MaterialForm' ]

class MaterialForm(Form):

	def clean(self):

		Form.clean(self)

		if 'link' in self.cleaned_data and 'content' in self.cleaned_data:
			raise ValidationError(_('Cannot set a document and an external link in the same material'))
		elif 'link' not in self.cleaned_data and 'content' in self.cleaned_data:
			raise ValidationError(_('Cannot upload an empty material'))

	class Meta(object):

		model = Material

		fields = [
			'title',
			'content',
			'link',
			'description',
			'suggested_ages',
			'types',
			'themes',
			'languages'
		]
		widgets = {
			'title': TextInput(attrs = { 'placeholder': _('1) Escribe el titulo') }),
			'link': URLInput(attrs = { 'placeholder': _('Content link (optional)') }),
			'description': Textarea(attrs = { 'placeholder': _('2) Escribe la descripción') }),
			'suggested_ages': CheckboxSelectMultiple(),
			'types': CheckboxSelectMultiple(),
			'themes': CheckboxSelectMultiple(),
			'languages':CheckboxSelectMultiple()
		}

