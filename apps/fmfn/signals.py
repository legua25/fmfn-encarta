from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth import get_user_model
from apps.fmfn.models import (
	Role,
	Campus,
	Material,
	Rating,
	Download,
)

User = get_user_model()

def users_to_remind(self):
	users = []
	for download in Download.objects.get(active=1):
		if download.material not in Rating.objects.get(active=1):
			users.append(download.user)

	return users

@receiver(user_logged_in)
def send_reminders(sender, user, request, **kwargs):
	pass