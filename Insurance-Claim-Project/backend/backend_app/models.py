from django.contrib.auth.models import AbstractUser
from django.db.models import Model, CASCADE, OneToOneField, IntegerField


class UserProfile(AbstractUser):
    permission_level = IntegerField(default=0)


class EndUser(Model):
    user = OneToOneField(UserProfile, on_delete=CASCADE)

    def save(self, *args, **kwargs):
        if not self.user.permission_level:
            self.user.permission_level = 3
        super().save(*args, **kwargs)
        self.user.save()


class AiEngineer(Model):
    user = OneToOneField(UserProfile, on_delete=CASCADE)

    def save(self, *args, **kwargs):
        if not self.user.permission_level:
            self.user.permission_level = 2
        super().save(*args, **kwargs)
        self.user.save()


class Finance(Model):
    user = OneToOneField(UserProfile, on_delete=CASCADE)

    def save(self, *args, **kwargs):
        if not self.user.permission_level:
            self.user.permission_level = 1
        super().save(*args, **kwargs)
        self.user.save()


class Administrator(Model):
    user = OneToOneField(UserProfile, on_delete=CASCADE)

    def save(self, *args, **kwargs):
        if not self.user.permission_level:
            self.user.permission_level = 0
        super().save(*args, **kwargs)
        self.user.save()
