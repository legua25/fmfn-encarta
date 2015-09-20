# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db.models import *
from django.conf import settings
from _base import Model

class Portfolio(Model):

    materials = ManyToManyField('fmfn.Material',
        related_name = '+',
        verbose_name = _('materials')
    )

    user = ForeignKey(settings.AUTH_USER_MODEL,
        related_name = 'portfolio',
        verbose_name = _('user')
    )

    class Meta(object):

        verbose_name = _('portfolio')
        verbose_name_plural = _('portfolios')
        app_label = 'fmfn'
