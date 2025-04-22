from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password
from backend_app.models import (
    UserProfile, EndUser, AiEngineer, Finance, Administrator,
    WeatherCondition, VehicleType, InjuryDescription, Gender,
    UserClaims
)
import random


class Command(BaseCommand):
    help = "Creates dummy data for testing purposes."

    def handle(self, *args, **kwargs):
        if UserProfile.objects.exists():
            self.stdout.write(self.style.WARNING("Dummy data already exists."))
            return

        self.stdout.write(" Creating dummy data")

        # Step 1: Base reference tables
        genders = ['Male', 'Female', 'Other']
        vehicle_types = ['Sedan', 'SUV', 'Truck']
        weather_conditions = ['Clear', 'Rainy', 'Snowy']
        injury_descriptions = ['Minor fracture', 'Severe concussion', 'Sprain']

        gender_objs = [Gender.objects.create(gender=g) for g in genders]
        vehicle_objs = [VehicleType.objects.create(vehicle_name=v) for v in vehicle_types]
        weather_objs = [WeatherCondition.objects.create(condition=w) for w in weather_conditions]
        injury_objs = [InjuryDescription.objects.create(description=d) for d in injury_descriptions]

        # Step 2: Users and roles
        admin_user = UserProfile.objects.create(
            username='admin_user',
            email='admin@example.com',
            password=make_password('adminpass123'),
        )
        Administrator.objects.create(user=admin_user)

        finance_user = UserProfile.objects.create(
            username='finance_user',
            email='finance@example.com',
            password=make_password('finance123'),
        )
        Finance.objects.create(user=finance_user)

        ai_user = UserProfile.objects.create(
            username='ai_engineer',
            email='ai@example.com',
            password=make_password('ai123'),
        )
        AiEngineer.objects.create(user=ai_user)

        end_user = UserProfile.objects.create(
            username='end_user',
            email='user@example.com',
            password=make_password('user123'),
        )
        EndUser.objects.create(user=end_user)

        # Step 3: Dummy claims for end_user
        for i in range(3):
            UserClaims.objects.create(
                user=end_user,
                passengers_involved=random.randint(1, 4),
                psychological_injury=random.choice([True, False]),
                injury_prognosis=round(random.uniform(1.0, 5.0), 1),
                injury_description=random.choice(injury_objs),
                exceptional_circumstance=random.choice([True, False]),
                whiplash=random.choice([True, False]),
                vehicle_type=random.choice(vehicle_objs),
                weather_condition=random.choice(weather_objs),
                driver_age=random.randint(18, 70),
                vehicle_age=random.randint(1, 15),
                police_report=random.choice([True, False]),
                witness_present=random.choice([True, False]),
                gender=random.choice(gender_objs)
            )

        self.stdout.write(self.style.SUCCESS(" Dummy data created successfully."))
