# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model
from apps.fmfn.models import Language
from django.forms import *
from django.forms import ModelForm as Form

__all__ = [ 'UserForm' ]
User = get_user_model()

class UserForm(Form):

	class Meta(object):

		model = Language
		fields = [
			'name'
		]
		widgets = {
			'name': TextInput(attrs = { 'placeholder': _('Tag name') }),
		}
