# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django_select2.forms import Select2MultipleWidget
from apps.fmfn.models import Material
from django.forms import *
from django.forms import ModelForm as Form

__all__ = [ 'MaterialForm' ]

class MaterialForm(Form):

	def clean(self):

		cleaned_data = Form.clean(self)

		content = cleaned_data.get('content')
		link = cleaned_data.get('link')

		if content and link: raise ValidationError({ 'content': _('El material debe tener al menos un link o documento, pero no ambos') })
		if not content and not link: raise ValidationError({ 'content': _('El material debe tener al menos un link o documento, pero no ambos') })

	class Meta(object):

		model = Material
		fields = [
			'title',
			'description',
			'content',
			'link',
			'suggested_ages',
			'types',
			'themes',
			'languages',
			'user'
		]
		widgets = {
			'title': TextInput(attrs = { 'placeholder': _('Título del material') }),
			'description': Textarea(attrs = { 'placeholder': _('Breve descripción del material'), 'rows': 6, 'style': 'resize: none;' }),
			'content': ClearableFileInput(attrs = { 'placeholder': _('Documentation') }),
			'link': URLInput(attrs = { 'placeholder': _('Link a referencia en formato http') }),
			'suggested_ages': CheckboxSelectMultiple(),
			'types': CheckboxSelectMultiple(),
			'themes': Select2MultipleWidget(),
			'languages': CheckboxSelectMultiple(),
			'user': HiddenInput()
		}