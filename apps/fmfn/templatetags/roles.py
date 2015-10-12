# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.template import Library

register = Library()

@register.filter
def has_role(user, role_name):
	return user.belongs_to(role_name)
