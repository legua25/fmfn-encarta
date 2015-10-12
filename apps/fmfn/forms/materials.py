# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django_select2.forms import Select2MultipleWidget
from apps.fmfn.models import Material, Theme, Type, Language
from django.forms import *
from django.forms import ModelForm as Form

__all__ = [ 'MaterialForm' ]

class MaterialForm(Form):

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
			'title': TextInput(attrs = { 'placeholder': _('Material title') }),
			'description': Textarea(attrs = { 'placeholder': _('Brief description on this material'), 'rows': 6, 'style': 'resize: none;' }),
			'content': ClearableFileInput(attrs = { 'placeholder': _('Documentation') }),
			'link': URLInput(attrs = { 'placeholder': _('Link to reference') }),
			'suggested_ages': CheckboxSelectMultiple(),
			'types': CheckboxSelectMultiple(),  # TODO: This will be replaced for Select2's implementation later
			'themes': Select2MultipleWidget,  # TODO: This will be replaced for Select2's implementation later
			'languages': CheckboxSelectMultiple(),  # TODO: This will be replaced for Select2's implementation later
			'user': HiddenInput()
		}
