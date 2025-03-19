from django.contrib.auth.models import AbstractUser
from django.db.models import Model, CASCADE, OneToOneField, IntegerField, BooleanField, CharField, ForeignKey, \
    DateTimeField, Sum
from django.utils import timezone


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


class VehicleType(Model):
    vehicle_name = CharField()


class WeatherCondition(Model):
    condition = CharField()


class ClaimTrainingData(Model):
    settle_value = IntegerField(default=0)
    accident_type = IntegerField(default=0)
    injury_prognosis_months = IntegerField(default=0)
    exceptional_circumstance = BooleanField(default=False)
    psychological_injury = BooleanField(default=False)
    dominant_injury = IntegerField(default=0)
    whiplash = BooleanField(default=False)
    vehicle_type = ForeignKey(VehicleType, on_delete=CASCADE)
    weather_condition = ForeignKey(WeatherCondition, on_delete=CASCADE, default=None)
    vehicle_age = IntegerField(default=0)
    driver_age = IntegerField(default=0)
    num_passengers = IntegerField(default=1)
    police_report = BooleanField(default=False)
    witness_present = BooleanField(default=False)
    gender = IntegerField(default=0)


class UserClaims(Model):
    user = ForeignKey(UserProfile, default=None, on_delete=CASCADE)
    passengers_involved = IntegerField(default=0)
    psychological_injury = BooleanField(default=False)
    injury_prognosis_months = IntegerField(default=0)
    exceptional_circumstance = BooleanField(default=False)
    dominant_injury = IntegerField(default=0)
    whiplash = BooleanField(default=False)
    vehicle_type = ForeignKey(VehicleType, on_delete=CASCADE)
    weather_condition = ForeignKey(WeatherCondition, on_delete=CASCADE)
    driver_age = IntegerField(default=0)
    vehicle_age = IntegerField(default=0)
    police_report = BooleanField(default=False)
    witness_present = BooleanField(default=False)
    gender = IntegerField(default=0)


class Actions(Model):
    action = CharField()


class UsageLog(Model):
    action = ForeignKey(Actions, on_delete=CASCADE)
    user = ForeignKey(UserProfile, on_delete=CASCADE, null=True, blank=True)
    time = DateTimeField(default=timezone.now)


class Invoice(Model):
    user = ForeignKey(UserProfile, on_delete=CASCADE)  # Link to the user
    total_amount = IntegerField(default=0)  # Sum of all claims
    created_at = DateTimeField(default=timezone.now)

    # currently only uses example data !
    # eventually change to settlement sum ! + additional info
    def calculate_total(self):
        claims = UserClaims.objects.filter(user=self.user)
        self.total_amount = claims.aggregate(Sum('passengers_involved'))['passengers_involved__sum'] or 0
        self.save()
