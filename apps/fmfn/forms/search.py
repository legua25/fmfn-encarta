# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from apps.fmfn.models import (
	Type,
	Theme,
	Language,
	SchoolGrade
)
from django.utils.translation import ugettext_lazy as _
from django_select2.forms import Select2MultipleWidget
from django.forms import *

__all__ = ['SearchForm']


class SearchForm(Form):
	search = CharField(
		required = False,
		widget = TextInput(attrs = {'placeholder': _('i.e. Harry Potter')})
	)
	grades = ModelMultipleChoiceField(
		queryset = SchoolGrade.objects.active(),
		required = False,
		widget = CheckboxSelectMultiple()
	)
	type = ModelMultipleChoiceField(
		queryset = Type.objects.active(),
		required = False,
		widget = CheckboxSelectMultiple()
	)
	language = ModelMultipleChoiceField(
		queryset = Language.objects.active(),
		required = False,
		widget = CheckboxSelectMultiple()
	)
	theme = ModelMultipleChoiceField(
		queryset = Theme.objects.active(),
		required = False,
		widget = Select2MultipleWidget()
	)
