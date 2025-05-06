import random
from datetime import date, timedelta

from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password

from backend_app.models import (
    Gender, VehicleType, WeatherCondition, InjuryDescription,
    UserProfile, AiEngineer, Administrator, EndUser, UserClaims
)

from backend_app.ML_model.model_utils import predict_settlement


class Command(BaseCommand):
    help = "Creates dummy data for testing purposes."

    def handle(self, *args, **kwargs):
        if UserProfile.objects.exists():
            self.stdout.write(self.style.WARNING("Dummy data already exists."))
            return

        self.stdout.write("Creating dummy data")

        # Reference data
        genders = ['Male', 'Female', 'Other']
        vehicle_types = ['Car', 'Motorcycle', 'Truck']
        weather_conditions = ['Sunny', 'Rainy', 'Snowy']
        injury_descriptions = [
            'Whiplash and minor bruises.', 'Minor cuts and scrapes.',
            'Concussion and bruised ribs.', 'Sprained ankle and wrist.'
        ]

        gender_objs = [Gender.objects.create(gender=g) for g in genders]
        vehicle_objs = [VehicleType.objects.create(vehicle_name=v) for v in vehicle_types]
        weather_objs = [WeatherCondition.objects.create(condition=w) for w in weather_conditions]
        injury_objs = [InjuryDescription.objects.create(description=d) for d in injury_descriptions]

        # AI Engineer
        ai_user = UserProfile.objects.create(
            username='drfirst',
            email='dr.first@ufcfur_15_3.com',
            password=make_password('ai123'),
        )
        AiEngineer.objects.create(user=ai_user)

        # Administrator
        admin_user = UserProfile.objects.create(
            username='anadmin',
            email='an.admin@ufcfur_15_3.com',
            password=make_password('admin123'),
        )
        Administrator.objects.create(user=admin_user)

        # End users
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

            for _ in range(2):
                acc_date = date.today() - timedelta(days=random.randint(1, 30))
                claim_date = acc_date + timedelta(days=random.randint(0, 10))
                gender = random.choice(gender_objs)
                vehicle_type = random.choice(vehicle_objs)
                weather_condition = random.choice(weather_objs)
                total_special_costs = round(random.uniform(300.0, 1500.0), 2)
                general_rest = round(random.uniform(100.0, 800.0), 2)
                general_fixed = round(random.uniform(50.0, 600.0), 2)

                claim_data = {
                    'passengers_involved': random.randint(1, 4),
                    'psychological_injury': random.choice([True, False]),
                    'injury_prognosis': round(random.uniform(1.0, 5.0), 1),
                    'exceptional_circumstance': random.choice([True, False]),
                    'whiplash': random.choice([True, False]),
                    'vehicle_type': vehicle_type,
                    'weather_condition': weather_condition,
                    'driver_age': random.randint(18, 70),
                    'vehicle_age': random.randint(1, 15),
                    'witness_present': random.choice([True, False]),
                    'gender': gender,
                    'total_special_costs': total_special_costs,
                    'general_rest': general_rest,
                    'general_fixed': general_fixed,
                    'accident_date': acc_date,
                    'claim_date': claim_date,
                }

                predict_input = {
                    'Driver Age': claim_data['driver_age'],
                    'Vehicle Age': claim_data['vehicle_age'],
                    'Injury_Prognosis': claim_data['injury_prognosis'],
                    'Whiplash': 'Yes' if claim_data['whiplash'] else 'No',
                    'Exceptional_Circumstances': 'Yes' if claim_data['exceptional_circumstance'] else 'No',
                    'Witness Present': 'Yes' if claim_data['witness_present'] else 'No',
                    'Vehicle Type': vehicle_type.vehicle_name,
                    'Weather Conditions': weather_condition.condition,
                    'Gender': gender.gender,
                    'Accident Date': acc_date,
                    'Claim Date': claim_date,
                    'TotalSpecialCosts': total_special_costs,
                    'GeneralRest': general_rest,
                    'GeneralFixed': general_fixed,
                    'Number of Passengers': claim_data['passengers_involved'],
                    'Minor_Psychological_Injury': 'Yes' if claim_data['psychological_injury'] else 'No',
                    'GeneralUplift': 0.0,
                }

                try:
                    settlement_value = predict_settlement(predict_input)
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"Prediction failed: {e}"))
                    settlement_value = None

                UserClaims.objects.create(
                    user=user,
                    predicted_settlement_value=settlement_value,
                    **claim_data
                )

        self.stdout.write(self.style.SUCCESS("Dummy data created successfully."))
