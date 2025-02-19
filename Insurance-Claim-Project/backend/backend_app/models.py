from django.contrib.auth.models import AbstractUser
from django.db.models import Model, CASCADE, OneToOneField, IntegerField, BooleanField, ForeignKey


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


class ClaimTrainingData(Model):
    settle_value = IntegerField(default=0)
    accident_type = IntegerField(default=0)
    injury_prognosis_months = IntegerField(default=0)
    exceptional_circumstance = BooleanField(default=False)
    psychological_injury = BooleanField(default=False)
    dominant_injury = IntegerField(default=0)
    whiplash = BooleanField(default=False)
    vehicle_type = IntegerField(default=0)
    weather_conditions = IntegerField(default=0)
    vehicle_age = IntegerField(default=0)
    driver_age = IntegerField(default=0)
    num_passengers = IntegerField(default=1)
    police_report = BooleanField(default=False)
    witness_present = BooleanField(default=False)
    gender = IntegerField(default=0)


class UserClaims(Model):
    user = ForeignKey(UserProfile, on_delete=CASCADE)
    passengers_involved = IntegerField(default=0)
    psychological_injury = BooleanField(default=False)
    exceptional_circumstance = BooleanField(default=False)
    dominant_injury = IntegerField(default=0)
    whiplash = BooleanField(default=False)
    vehicle_type = IntegerField(default=0)
    weather_condition = IntegerField(default=0)
    driver_age = IntegerField(default=0)
    vehicle_age = IntegerField(default=0)
    gender = IntegerField(default=0)
