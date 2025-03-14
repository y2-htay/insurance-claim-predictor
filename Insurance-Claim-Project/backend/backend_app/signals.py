from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

from .models import UsageLog, Actions, UserProfile, ClaimTrainingData, WeatherCondition, VehicleType


def log_action(action_text):
    action, _ = Actions.objects.get_or_create(action=action_text)
    UsageLog.objects.create(action=action)


@receiver(user_logged_in)
def log_user_login(**kwargs):
    log_action("User Logged In")


@receiver(user_logged_out)
def log_user_logout(**kwargs):
    log_action("User Logged Out")


@receiver(post_save, sender=UserProfile)
def log_user_change(created, **kwargs):
    if created:
        log_action("User Created")
    else:
        log_action("User Updated")


@receiver(post_delete, sender=UserProfile)
def log_user_deletion(**kwargs):
    log_action("User Deleted")


@receiver(post_save, sender=ClaimTrainingData)
def log_dataset_change(created, **kwargs):
    if created:
        log_action("Training data created")
    else:
        log_action("Training data updated")


@receiver(post_delete, sender=ClaimTrainingData)
def log_dataset_deletion(**kwargs):
    log_action("Training data deleted")


@receiver(post_save, sender=WeatherCondition)
def log_weather_change(created, **kwargs):
    if created:
        log_action("Weather condition table created")
    else:
        log_action("Weather condition table updated")


@receiver(post_delete, sender=WeatherCondition)
def log_weather_deletion(**kwargs):
    log_action("Weather condition data deleted")


@receiver(post_save, sender=VehicleType)
def log_vehicle_data_change(created, **kwargs):
    if created:
        log_action("Vehicle type table created")
    else:
        log_action("Vehicle type table updated")


@receiver(post_delete, sender=VehicleType)
def log_vehicle_data_deletion(**kwargs):
    log_action("Vehicle type data deleted")
