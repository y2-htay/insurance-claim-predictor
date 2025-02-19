from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Model


class UserProfile(AbstractUser):
    permission_level = models.IntegerField(default=0)


class EndUser(Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)


class AiEngineer(Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)


class Administrator(Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)


class Finance(Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)
