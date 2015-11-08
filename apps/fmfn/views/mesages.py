# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from apps.fmfn.models import (
	Material,
	Comment,
	ActionLog,
	Role,
)
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.views.generic import View
from celery import Celery
from celery.schedules import crontab
import datetime

User = get_user_model()
app = Celery()

CELERY_TIMEZONE = 'CST'

CELERYBEAT_SCHEDULE = {
    'add-every-monday-morning': {
        'task': 'tasks.add',
        'schedule': crontab(hour=8, minute=30, day_of_week=1),
        'args': (16, 16),
    },
}

class CommentReportView(View):

	def send_comment_report(self):

		role = Role.objects.active().filter(name = "administrator")
		users = User.objects.active().filter(role=role)
		emails = []
		#get all the administrators' email in a list
		for user in users:
			emails.extend(user)

		end = datetime.datetime.now()
		start = end - datetime.timedelta(days=7)
		comments = Comment.objects.active().filter(date_created__range=[start, end])
		materials = []
		#get all materials with comments published in date range to a list
		for comment in comments:
			if comment.material not in materials:
				materials.extend(comment.material)


		body = render_to_string('email_report.html', context = locals())
		ActionLog.objects.log_account('Sending comment report to user', user = users, status = 201)

		mail = EmailMultiAlternatives(
			subject = _('Materials reviewed this week'),
			body = body,
			to = [users]
		)
		mail.attach_alternative(body, 'text/html')
		mail.send(True)

comment_report = CommentReportView.as_view()