# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.utils.http import urlsafe_base64_encode as base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.utils.translation import ugettext_lazy as _
from django.utils.crypto import constant_time_compare
from django.contrib.auth.models import AnonymousUser
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from django.shortcuts import RequestContext
from django.utils.http import force_bytes
from apps.fmfn.models import ActionLog
from django.forms import *

__all__ = [ 'LoginForm', 'RecoveryForm' ]
User = get_user_model()

class LoginForm(Form):

	email_address = EmailField(
		max_length = 255,
		required = True,
		widget = EmailInput(attrs = { 'placeholder': _('Correo electrónico') })
	)
	password = CharField(
		max_length = 128,
		required = True,
		widget = PasswordInput(attrs = { 'placeholder': _('Contraseña') })
	)
	user = AnonymousUser()

	def clean(self):

		email, password = self.cleaned_data['email_address'], self.cleaned_data['password']
		user = authenticate(email_address = email, password = password)

		if user is not None:

			if user.is_active: self.user = user
			else: raise ValidationError(_('El usuario no se encuentra activo en el sistema'))

		else: raise ValidationError(_('Correo electronico/contraseña erronea'))

class RecoveryForm(Form):

	email_address = EmailField(
		max_length = 255,
		required = True,
		widget = EmailInput(attrs = { 'placeholder': _('Correo electrónico') })
	)
	password = CharField(
		max_length = 128,
		required = True,
		widget = PasswordInput(attrs = { 'placeholder': _('Nueva Contraseña') })
	)
	repeat = CharField(
		max_length = 128,
		required = True,
		widget = PasswordInput(attrs = { 'placeholder': _('Repetir Contraseña') })
	)

	user = AnonymousUser()

	def __init__(self, *args, **kwargs):

		self.user = kwargs.pop('user', AnonymousUser())
		self._stage = stage = kwargs.pop('stage', '')

		Form.__init__(self, *args, **kwargs)

		if stage == 'reset': del self.fields['email_address']
		elif stage == 'recover':

			del self.fields['password']
			del self.fields['repeat']
		else: raise ValueError('Valor invalido (esperaba: "recover" or "complete", recibió: %s)' % stage)

	def clean(self):

		if self._stage == 'recover':

			# Locate the user account by email address
			email = self.cleaned_data['email_address']

			try: user = User.objects.get(email_address = email)
			except User.DoesNotExist: raise ValidationError(_('El correo que ingresaste no tiene registros en nuestro sitio'))
			else:

				if user.is_active: self.user = user
				else: raise ValidationError(_('Esta cuenta de usuario ha sido desactivada. Por favor contacte a su administrador para más información.'))

		elif self._stage == 'reset':

			if self.user is None or isinstance(self.user, AnonymousUser):
				raise ValueError('No se encontró un usuario que coincidiera')

			# Validate passwords are equal and different from user's
			password, repeat = [ self.cleaned_data['password'], self.cleaned_data['repeat'] ]

			if not constant_time_compare(password, repeat): raise ValidationError('Las contraseñas no coinciden')
			elif self.user.check_password(password): raise ValidationError('La nueva contraseña esta actualmente siendo usada')

		else: raise ValidationError('Instancia invalida')
	def send_recovery_email(self, request, user, token):

		# Get mailing information and next step data
		site = get_current_site(request)
		domain = site.domain
		protocol = ('https' if request.is_secure() else 'http')
		user_id = base64_encode(force_bytes(user.id))

		# Create the actual email
		body = render_to_string('accounts/email_recover.html', context = RequestContext(request, locals()))
		ActionLog.objects.log_account('Sending recovery email to user', user = user, status = 201)

		mail = EmailMultiAlternatives(
			subject = _('Recuperacion de contraseña - Sistema NWL'),
			body = body,
			to = [ user.email_address ]
		)
		mail.attach_alternative(body, 'text/html')
		mail.send(True)
