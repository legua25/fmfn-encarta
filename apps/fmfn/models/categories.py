# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db.models import *
from django.utils.translation import ugettext_lazy as _

class Category(Model):

    title = CharField(
        max_length = 64,
        unique = True,
        null = False,
        blank = False
    )

    material = ManyToManyField('fmfn.Material',
        related_name = 'categories',
        verbose_name =  _('materials'),
        null = False
    )
