from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import UsageLog, Actions


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    action, created = Actions.objects.get_or_create(action='User Logged In')
    UsageLog.objects.create(user=user, action=action)
