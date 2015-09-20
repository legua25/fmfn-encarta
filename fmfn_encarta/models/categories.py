from django.db.models import *
from django.utils.translation import ugettext_lazy as _

class Category(Model):

    title = CharField(
        max_length = 64,
        unique = True,
        null = False,
        blank = False
    )

    material = ManyToManyField('fmfn_encarta.Material',
        related_name='materials',
        verbose_name= _('materials'),
        null=False
    )
