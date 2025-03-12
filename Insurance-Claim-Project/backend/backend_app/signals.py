from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import UsageLog, Actions, UserProfile, ClaimTrainingData


def log_action(user, action_text):
    if user and user.is_authenticated:
        action, _ = Actions.objects.get_or_create(action=action_text)
        UsageLog.objects.create(user=user, action=action)


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    log_action(user, "User Logged In")


@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    log_action(user, "User Logged Out")


@receiver(post_save, sender=UserProfile)
def log_user_creation(sender, instance, created, **kwargs):
    if created:
        log_action(instance, "User Created")
    else:
        log_action(instance, "User Updated")


@receiver(post_delete, sender=UserProfile)
def log_user_deletion(sender, instance, **kwargs):
    log_action(instance, "User Deleted")


@receiver(post_save, sender=ClaimTrainingData)
def log_dataset_change(sender, instance, **kwargs):
    log_action(instance, action_text="Training data changed")


def log_dataset_deletion(sender, instance, **kwargs):
    log_action(instance, "Training data deleted")
