from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Model, CASCADE, OneToOneField, IntegerField, BooleanField, CharField, ForeignKey, \
    DateTimeField, Sum, FileField, FloatField
from django.utils import timezone
from django.conf import settings
from django.db.models import DateField

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


class Gender(Model):
    gender = CharField(unique=True)


class InjuryDescription(Model):
    description = CharField(unique=True)


class VehicleType(Model):
    vehicle_name = CharField(unique=True)


class WeatherCondition(Model):
    condition = CharField(unique=True)


class ClaimTrainingData(Model):
    data_file = FileField(upload_to='training_data/')


class UserClaims(models.Model):
    user = models.ForeignKey('UserProfile', default=None, on_delete=models.CASCADE)
    
    passengers_involved = models.FloatField(default=0)
    psychological_injury = models.BooleanField(default=False)
    injury_prognosis = models.FloatField(default=0)
    exceptional_circumstance = models.BooleanField(default=False)
    whiplash = models.BooleanField(default=False)
    witness_present = models.BooleanField(default=False)
    vehicle_type = models.ForeignKey('VehicleType', on_delete=models.CASCADE)
    weather_condition = models.ForeignKey('WeatherCondition', on_delete=models.CASCADE)
    gender = models.ForeignKey('Gender', on_delete=models.CASCADE)
    driver_age = models.FloatField(default=0)
    vehicle_age = models.FloatField(default=0)
    total_special_costs = models.FloatField(default=0)
    general_rest = models.FloatField(default=0)       
    general_fixed = models.FloatField(default=0)       
    accident_date = models.DateField()
    claim_date = models.DateField()
    predicted_settlement_value = models.FloatField(null=True, blank=True)
    supporting_documents = models.FileField(upload_to='documents/', null=True, blank=True)



class Actions(Model):
    action = CharField()


class UsageLog(Model):
    action = ForeignKey(Actions, on_delete=CASCADE)
    user = ForeignKey(UserProfile, on_delete=CASCADE, default=None)
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


class InsuranceModel(Model):
    model_file = models.FileField(upload_to='models/')


# feedback model
class UserFeedback(Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback from {self.user} on {self.created_at.strftime('%Y-%m-%d')}"
