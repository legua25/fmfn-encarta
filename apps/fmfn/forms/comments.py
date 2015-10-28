# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django_select2.forms import Select2MultipleWidget
from apps.fmfn.models import Comment
from django.forms import *
from django.forms import ModelForm as Form

__all__ = [ 'CommentForm' ]

class CommentForm(Form):

	class Meta(object):

		model = Comment
		fields = [ 'content', 'rating_value', 'user', 'material' ]
		widgets = {
			'user': HiddenInput(),
			'material': HiddenInput(),
			'content': Textarea(attrs = { 'placeholder': _('Write a comment here'), 'rows': 6, 'style': 'resize: none;' }),
			'rating_value': RadioSelect()
		}
