# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from apps.fmfn.models import (
	Comment,
	ActionLog,
	Role,
	Material
)
from django.utils.translation import ugettext_lazy as _
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from celery.utils.log import get_task_logger
from fmfn_encarta.settings import app
from django.utils.timezone import now
from datetime import timedelta

User = get_user_model()
logger = get_task_logger(__name__)

@app.task
def send_report(self):
	"""
	This task collects every material commented in the past week and sends a report to the system administrator every Monday morning
	"""
	role = Role.objects.active().filter(name = "administrator")
	users = User.objects.active().filter(role = role)
	today = now()
	#get materials with comments created between today and 8 days ago
	materials = Material.objects.active().filter(comments__date_created__range = [(today - timedelta(days = 8)), today])

	#get all materials with comments published in date range to a list
	recently_commented = { c for c in materials }

	if len(recently_commented) > 0:
		#get all the administrators' email in a list
		emails = [ u.email_address for u in users ]
		for u in emails:
			logger.info('Sending email to %s' % u)
			#ActionLog.objects.log_account('Sending comment report to user', user = u, status = 201)

		body = render_to_string('email_report.html', context = locals())
		mail = EmailMultiAlternatives(
			subject = _('Materiales comentados de la semana'),
			body = body,
			to = emails
		)
		mail.attach_alternative(body, 'text/html')
		mail.send(True)