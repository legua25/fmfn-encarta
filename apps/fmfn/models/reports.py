# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db.models import *
from django.conf import settings
from _base import Model

# settings.AUTH_USER_MODEL

class Report(Model):
    user = ForeignKey(settings.AUTH_USER_MODEL,
                      related_name='reports',
                      verbose_name='author'
                      )

    description = CharField(
        max_length=64
    )

    material = ForeignKey('fmfn.Material',
                          related_name='reports',
                          verbose_name='reported material'
                          )


    class Meta(object):
        verbose_name = 'material report'
        verbose_name_plural = 'material reports'
        app_label = 'fmfn'
