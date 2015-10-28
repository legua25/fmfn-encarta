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

def unreviewed_materials(user):
	# Query comments for materials filtered by user
	# Store a list of the id's of the materials
	# Query downloads for materials filtered by user
	# Store a list of the id's of the materials
	# id's on the second list that are not in the first are the unreviewed materials for user
	pass

@receiver(user_logged_in)
def send_reminders(sender, user, request, **kwargs):
	pass