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

        self.stdout.write("Creating dummy data")

        # Step 1: Base reference tables
        genders = ['Male', 'Female', 'Other']
        vehicle_types = ['Car', 'Motorcycle', 'Truck']
        weather_conditions = ['Sunny', 'Rainy', 'Snowy']
        injury_descriptions = ['Whiplash and minor bruises.', 'Minor cuts and scrapes.', 'Concussion and bruised ribs.', 'Sprained ankle and wrist.']

        gender_objs = [Gender.objects.create(gender=g) for g in genders]
        vehicle_objs = [VehicleType.objects.create(vehicle_name=v) for v in vehicle_types]
        weather_objs = [WeatherCondition.objects.create(condition=w) for w in weather_conditions]
        injury_objs = [InjuryDescription.objects.create(description=d) for d in injury_descriptions]

        # Step 2: AI Engineer
        ai_user = UserProfile.objects.create(
            username='drfirst',
            email='dr.first@ufcfur_15_3.com',
            password=make_password('ai123'),
        )
        AiEngineer.objects.create(user=ai_user)

        # Step 3: Administrator
        admin_user = UserProfile.objects.create(
            username='anadmin',
            email='an.admin@ufcfur_15_3.com',
            password=make_password('admin123'),
        )
        Administrator.objects.create(user=admin_user)

        # Step 4: End users (clients)
        client_names = [
            ('robsmith', 'Mr Rob Smith'),
            ('lizbrown', 'Ms Liz Brown'),
            ('hesitant', 'Mr Hesitant'),
            ('janesnow', 'Ms Jane Snow'),
            ('joeblack', 'Mr Joe Black'),
            ('clairewhite', 'Ms Claire White'),
            ('harrypotts', 'Mr Harry Potts'),
            ('lucybell', 'Ms Lucy Bell'),
            ('mattgrey', 'Mr Matt Grey'),
            ('fionared', 'Ms Fiona Red')
        ]

        for username, full_name in client_names:
            user = UserProfile.objects.create(
                username=username,
                email=f'{username}@example.com',
                password=make_password('client123'),
                first_name=full_name.split()[1],
                last_name=full_name.split()[-1]
            )
            EndUser.objects.create(user=user)

            # Step 5: Dummy claims per client
            for _ in range(2):  # 2 claims per client
                UserClaims.objects.create(
                    user=user,
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

        self.stdout.write(self.style.SUCCESS("Dummy data created successfully."))
