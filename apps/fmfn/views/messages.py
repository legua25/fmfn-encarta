# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from apps.fmfn.models import (
	Comment,
	ActionLog,
	Role,
)
from django.shortcuts import redirect, render_to_response, RequestContext
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.views.generic import View
from django.http import JsonResponse
from celery.schedules import crontab
from celery import Celery
import datetime

__all__ = [
	'comment_report',
]
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

	def get(self,request):

		role = Role.objects.active().filter(name = "administrator")
		users = User.objects.active().filter(role=role)
		emails = []
		#get all the administrators' email in a list
		for user in users:
			emails.append(user.email_address)
			ActionLog.objects.log_account('Sending comment report to user', user = user, status = 201)

		end = datetime.datetime.now()
		start = end - datetime.timedelta(days=7)
		comments = Comment.objects.active().filter(date_created__range=[start, end])
		materials = []
		#get all materials with comments published in date range to a list
		for comment in comments:
			if comment.material not in materials:
				materials.append(comment.material)

		if len(materials) > 0:

			body = render_to_string('email_report.html', context = locals())

			mail = EmailMultiAlternatives(
				subject=_('Materials reviewed this week'),
				body = body,
				to = [emails]
			)
			mail.attach_alternative(body, 'text/html')
			mail.send(True)
			return JsonResponse({
					'version': '1.0.0',
					'status': 201,
					'data': emails
				}, status = 201)
		else:
			return JsonResponse({
					'version': '1.0.0',
					'status': 201,
					'data': 'no recent comments'
				}, status = 201)

comment_report = CommentReportView.as_view()