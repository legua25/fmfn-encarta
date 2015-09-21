# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.translation import ugettext_lazy as _
from django.db.models import *
from django.conf import settings
from _base import Model

class Material(Model):

    """ Represents the model for the materials. It contains:
        *title(CharField): it's the title of the material
        *description(Charfield): it's the description of the material
        *suggested_ages(PositiveSmallIntegerField): the optional values here are related with the educational level
        *user (ForeignKey): A relationship to users to know if the material is visible to them
    """

    title = CharField(
        max_length = 128,
        null = False,
        blank = False
    )
    description = CharField(
        max_length = 1024,
        null = False,
        blank = False,
        verbose_name = _('description')
    )
    suggested_ages = PositiveSmallIntegerField(
        choices = [
            (1, _('kindergarten')),
            (2, _('pre school')),
            (3, _('low elementary school')),
            (4, _('high elementary school')),
            (5, _('junior high school'))
        ],
        verbose_name = _('suggested ages')
    )
    user = ForeignKey(settings.AUTH_USER_MODEL,
        related_name = 'materials',
        on_delete = CASCADE,
		verbose_name = _('uploading user')
	)

	class Meta(object):

		verbose_name = _('material')
		verbose_name_plural = _('materials')
		app_label = 'fmfn'
