import joblib
import os
import numpy as np
import pandas as pd
import sys
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
import traceback
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, 'final_stacked_model.joblib')
SCALER_PATH = os.path.join(BASE_DIR, 'scaler.joblib')
IMPUTER_PATH = os.path.join(BASE_DIR, 'num_imputer.joblib')
FEATURES_PATH = os.path.join(BASE_DIR, 'trained_columns.joblib')

# Load model and transformers
model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
imputer = joblib.load(IMPUTER_PATH)
trained_columns = joblib.load(FEATURES_PATH)

# Binary features
binary_columns = ["Exceptional_Circumstances", "Whiplash", "Witness Present"]

# Special cost fields used to compute TotalSpecialCosts
special_cost_fields = [
    'SpecialEarningsLoss', 'SpecialTherapy', 'SpecialAssetDamage',
    'SpecialTripCosts', 'SpecialJourneyExpenses', 'SpecialLoanerVehicle',
    'SpecialUsageLoss', 'SpecialFixes', 'SpecialOverage'
]

# Final numerical features used in model
numerical_cols = [
    'GeneralRest', 'Number of Passengers', 'GeneralFixed', 'GeneralUplift',
    'Driver Age', 'Injury_Prognosis', 'ClaimDelayDays', 'Vehicle Age',
    'TotalSpecialCosts', 'Driver_Vehicle_Interaction'
]

# Only the final categorical fields used in the model
categorical_cols = [
    'Vehicle Type', 'Weather Conditions', 'Gender',
    'Minor_Psychological_Injury', 'DriverAge_Bucket', 'VehicleAge_Bucket',
    'Injury_Severity_Level', 'ClaimSpeedCategory'
]

def extract_months(value):
    try:
        if isinstance(value, (int, float)):
            return value
        digits = ''.join(filter(str.isdigit, str(value)))
        return int(digits) if digits else np.nan
    except:
        return np.nan


def preprocess_input(data: dict) -> pd.DataFrame:
    df = pd.DataFrame([data])
    print("Input keys received:", list(data.keys()))
    sys.stdout.flush()

    # Ensure all special cost fields are present
    for field in special_cost_fields:
        if field not in df.columns:
            df[field] = 0.0

    # Date handling
    df['Accident Date'] = pd.to_datetime(df['Accident Date'], errors='coerce')
    df['Claim Date'] = pd.to_datetime(df['Claim Date'], errors='coerce')
    df['ClaimDelayDays'] = (df['Claim Date'] - df['Accident Date']).dt.days

    # Convert Injury_Prognosis
    df['Injury_Prognosis'] = df['Injury_Prognosis'].apply(extract_months)

    # Binary mapping
    for col in binary_columns:
        if col in df.columns:
            df[col] = df[col].map({"Yes": 1, "No": 0}).fillna(0)

    # Derived features
    df['TotalSpecialCosts'] = df[special_cost_fields].sum(axis=1)
    df['Driver_Vehicle_Interaction'] = df['Driver Age'] * df['Vehicle Age']
    df['DriverAge_Bucket'] = pd.cut(df['Driver Age'], bins=[0, 25, 45, 65, 100],
                                    labels=['<25', '25-45', '45-65', '65+'])
    df['VehicleAge_Bucket'] = pd.cut(df['Vehicle Age'], bins=[-1, 5, 10, 20, 100],
                                     labels=['0-5', '6-10', '11-20', '20+'])
    df['Injury_Severity_Level'] = pd.cut(df['Injury_Prognosis'], bins=[-1, 3, 6, 12, 60],
                                         labels=['Low', 'Medium', 'High', 'Very High'])
    df['ClaimSpeedCategory'] = pd.cut(df['ClaimDelayDays'], bins=[-10, 5, 15, 30, 999],
                                      labels=['Immediate', 'Fast', 'Normal', 'Late'])

    print("\n[DEBUG] Raw data before imputation and scaling:")
    print(df[['GeneralFixed', 'TotalSpecialCosts', 'GeneralRest', 'Injury_Prognosis']])
    sys.stdout.flush()

    # Impute and scale numericals
    df[numerical_cols] = imputer.transform(df[numerical_cols])
    df[numerical_cols] = scaler.transform(df[numerical_cols])

    # Fill missing categoricals
    for col in categorical_cols:
        if col in df.columns:
            df[col] = df[col].fillna(df[col].mode()[0])

    # One-hot encode categorical
    df = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

    # Reindex to match model input structure
    df = df.reindex(columns=trained_columns, fill_value=0)

    return df

def predict_settlement(data: dict) -> float:
    try:
        print("Raw input data:", data)
        X = preprocess_input(data)
        print("Processed input for model:", X)

        # Log the top 3 most important features
        print("Key features used:")
        print("  TotalSpecialCosts:", X['TotalSpecialCosts'].values[0])
        print("  GeneralRest:", X['GeneralRest'].values[0])
        print("  GeneralFixed:", X['GeneralFixed'].values[0])

        prediction = model.predict(X)[0]
        print("Prediction result:", prediction)
        sys.stdout.flush()
        return round(prediction, 2)
   
    except Exception as e:
        print("Prediction failed:", repr(e))  
        traceback.print_exc()
        sys.stdout.flush()
        return None
