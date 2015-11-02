# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from apps.fmfn.models import (
	Type,
	Theme,
	Language
)

admin.site.register(Type)
admin.site.register(Theme)
admin.site.register(Language)