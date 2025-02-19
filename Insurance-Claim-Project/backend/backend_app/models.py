from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Model


class UserProfile(AbstractUser):
    permission_level = models.IntegerField(default=0)


class EndUser(Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.user.permission_level:
            self.user.permission_level = 3
        super().save(*args, **kwargs)
        self.user.save()


class AiEngineer(Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.user.permission_level:
            self.user.permission_level = 2
        super().save(*args, **kwargs)
        self.user.save()


class Finance(Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.user.permission_level:
            self.user.permission_level = 1
        super().save(*args, **kwargs)
        self.user.save()


class Administrator(Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        if not self.user.permission_level:
            self.user.permission_level = 0
        super().save(*args, **kwargs)
        self.user.save()
