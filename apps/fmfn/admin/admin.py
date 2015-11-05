# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from apps.fmfn.models import (
	Type,
	Theme,
	Language,
	Portfolio,
	Item,
	SchoolGrade,
	Campus,
	Report,
	ActionLog,
	Download,
	Material,
	User,
	Role,
	Comment
)

# On this file, the models to be displayed on the django admin panel are registered:

# All models available:
admin.site.register(Type)
admin.site.register(Theme)
admin.site.register(Language)
admin.site.register(Portfolio)
admin.site.register(Item)
admin.site.register(SchoolGrade)
admin.site.register(Campus)
admin.site.register(Report)
admin.site.register(ActionLog)
admin.site.register(Download)
admin.site.register(Material)
admin.site.register(User)
admin.site.register(Role)
admin.site.register(Comment)