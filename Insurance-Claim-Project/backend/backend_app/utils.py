import io
from django.core.files.base import ContentFile
from django.db import transaction
import os
from .models import UserProfile, Gender, InjuryDescription, VehicleType, WeatherCondition
from backend_app.models import Actions, UsageLog
import pandas as pd
from sklearn.preprocessing import RobustScaler
from backend_app.models import ClaimTrainingData

redundant_labels = ['Accident Description', 'Claim Date', 'Accident Date',
                    'SpecialHealthExpenses', 'SpecialReduction', 'SpecialOverage', 'GeneralRest',
                    'SpecialAdditionalInjury', 'SpecialEarningsLoss', 'SpecialUsageLoss', 'SpecialMedications',
                    'SpecialAssetDamage', 'SpecialRehabilitation', 'SpecialFixes', 'GeneralFixed', 'GeneralUplift',
                    'SpecialLoanerVehicle', 'SpecialTripCosts', 'SpecialJourneyExpenses', 'SpecialTherapy']

category_labels = ['AccidentType', 'Exceptional_Circumstances', 'Minor_Psychological_Injury', 'Dominant injury',
                   'Whiplash', 'Vehicle Type', 'Weather Conditions',
                   'Police Report Filed', 'Witness Present', 'Gender', 'Injury Description']

numerical_labels = ['SettlementValue', 'Injury_Prognosis',
                    'Vehicle Age', 'Driver Age', 'Number of Passengers']


def log_action(action_text, user=None):
    action, _ = Actions.objects.get_or_create(action=action_text)
    UsageLog.objects.create(action=action, user=user)


def get_current_user(request):
    current_user = request.user
    user_profile = UserProfile.objects.get(id=current_user.id)
    return user_profile


def clean_dataset(data):
    data.dropna(inplace=True)
    data.drop(redundant_labels, axis=1, inplace=True)
    return data


def categorise_data(data, label):
    add_category_to_db(data, label)

    values = data[label].astype(str).str.lower()

    if values.nunique() == 2 and set(values.unique()) <= {'yes', 'no'}:
        data[label] = values.map({'yes': True, 'no': False})

    elif values.nunique() <= 5:
        data[label], _ = pd.factorize(data[label])

    else:
        categories = pd.get_dummies(data[label], prefix=label)
        data.drop(label, axis=1, inplace=True)
        data = pd.concat([data, categories], axis=1)
    return data


def extract_months(prognosis):
    return int(''.join(filter(str.isdigit, prognosis)))


def scale_data(data):
    scaler = RobustScaler()
    data[numerical_labels] = scaler.fit_transform(data[numerical_labels])
    return data


def add_category_to_db(data, label):
    unique_values = data[label].unique()
    with transaction.atomic():
        for value in unique_values:
            instance = None
            try:
                if label == 'Vehicle Type':
                    if not VehicleType.objects.filter(vehicle_name=value).exists():
                        instance = VehicleType(vehicle_name=value)
                elif label == 'Weather Conditions':
                    if not WeatherCondition.objects.filter(condition=value).exists():
                        instance = WeatherCondition(condition=value)
                elif label == 'Injury Description':
                    if not InjuryDescription.objects.filter(description=value).exists():
                        instance = InjuryDescription(description=value)
                elif label == 'Gender':
                    if not Gender.objects.filter(gender=value).exists():
                        instance = Gender(gender=value)
                if instance:
                    instance.save()
            except Exception as e:
                raise Exception(e)
    return True


def preprocess_data_and_upload(data):
    data = clean_dataset(data)
    data['Injury_Prognosis'] = data['Injury_Prognosis'].apply(extract_months)
    data = scale_data(data)
    for label in category_labels:
        data = categorise_data(data, label)

    # outlier removal
    upper_limit = data['SettlementValue'].quantile(0.90)
    lower_limit = data['SettlementValue'].quantile(0.10)
    data['SettlementValue'] = data['SettlementValue'].clip(lower=lower_limit, upper=upper_limit)

    try:
        csv_buffer = io.StringIO()
        data.to_csv(csv_buffer, index=False)
        csv_content = csv_buffer.getvalue()
        csv_file = ContentFile(csv_content.encode('utf-8'), name='processed.csv')

        # Retrieve the existing instance if it exists
        instance = ClaimTrainingData.objects.first()
        if instance and instance.data_file:
            if os.path.isfile(instance.data_file.path):
                os.remove(instance.data_file.path)
        else:
            instance = ClaimTrainingData()

        instance.data_file.save('processed.csv', csv_file)
        instance.save()
    except Exception as e:
        raise Exception("Could not upload training data!") from e
    else:
        return True
