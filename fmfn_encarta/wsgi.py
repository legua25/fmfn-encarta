 # -*- coding utf-8 -*-
from __future__ import unicode_literals
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fmfn_encarta.settings.product')
os.environ.setdefault('DJANGO_CONFIGURATION', 'Production')

from configurations.wsgi import get_wsgi_application
application = get_wsgi_application()
