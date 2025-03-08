from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .models import UsageLog, Actions


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    action, created = Actions.objects.get_or_create(action='User Logged In')
    UsageLog.objects.create(user=user, action=action)


@receiver(user_logged_out)
def log_user_logout(sender, request, **kwargs):
    action, created = Actions.objects.get_or_create(action='User Logged Out')
    UsageLog.objects.create(user=request.user, action=action)
