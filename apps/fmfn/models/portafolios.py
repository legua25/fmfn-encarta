# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db.models import *
from django.conf import settings

#settings.AUTH_USER_MODEL

class Portafolio(Model):
    materials = ManyToManyField('fmfn.Material',
    related_name = 'portafolio'
    )
    user = ForeignKey(settings.AUTH_USER_MODEL)

    class Meta(object):
        app_label = 'fmfn'
        verbose_name = 'portafolio'
        verbose_name_plural = 'portafolios'

