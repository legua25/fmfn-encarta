# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.admin import site
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

# All models available:
site.register(Type)
site.register(Theme)
site.register(Language)
site.register(Portfolio)
site.register(Item)
site.register(SchoolGrade)
site.register(Campus)
site.register(Report)
site.register(ActionLog)
site.register(Download)
site.register(Material)
site.register(User)
site.register(Role)
site.register(Comment)