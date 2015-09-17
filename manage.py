#!/usr/bin/env python
# -*- coding utf-8 -*-
from __future__ import unicode_literals
import os, sys

if __name__ == '__main__':

	os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fmfn_encarta.settings')
	os.environ.setdefault('DJANGO_CONFIGURATION', 'Development')

	from configurations import importer
	importer.install()

	from configurations.management import execute_from_command_line
	execute_from_command_line(sys.argv)
