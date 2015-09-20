# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db.models import *
from django.conf import settings

# Create your models here.
class Material(Model):

    title = CharField(
        max_length = 128,
        null = False,
        blank = False
    )

    description = CharField(
        max_length= 1024,
        null = False,
        blank = False,
        verbose_name = _('material description')
    )

    suggested_agee = PositiveSmallIntegerField(
        choices = [
            (1, _('kindergarten')),
            (2, _('pre school')),
            (3, _('low elementary school')),
            (4, _('high elementary school')),
            (5, _('junior high school'))
        ]
    )

    user = ForeignKey(settings.AUTH_USER_MODEL,
        null = False,
        on_delete = CASCADE
    )

    class Meta(object):

        verbose_name = _('material')
        verbose_name_plural = _('materials')
        app_label = 'fmfn'