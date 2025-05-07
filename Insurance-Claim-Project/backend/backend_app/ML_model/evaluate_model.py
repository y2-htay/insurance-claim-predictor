import os
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import euclidean_distances


def evaluate_model():
    # === Paths ===
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    TRAIN_PATH = os.path.join(BASE_DIR, 'train_data.csv')
    NEW_CLAIM_PATH = os.path.join(BASE_DIR, 'new_claim.csv')
    EVAL_PATH = os.path.join(BASE_DIR, 'evaluation_results.csv')

    # === Load Data ===
    train_df = pd.read_csv(TRAIN_PATH)
    new_df = pd.read_csv(NEW_CLAIM_PATH).tail(1)

    # === Ensure same columns ===
    common_columns = list(set(train_df.columns).intersection(set(new_df.columns)))
    if 'SettlementValue' in common_columns:
        common_columns.remove('SettlementValue')

    X_train = train_df[common_columns]
    y_train = train_df["SettlementValue"]

    X_new = new_df[common_columns]
    y_pred = new_df["SettlementValue"].values[0]  # predicted value already stored

    # === Top important features for similarity ===
    top_features = ['GeneralFixed', 'TotalSpecialCosts', 'GeneralRest', 'Injury_Prognosis']
    top_features = [f for f in top_features if f in common_columns]

    # === Find closest match ===
    distances = euclidean_distances(X_train[top_features], X_new[top_features])
    closest_idx = np.argmin(distances)
    y_true = y_train.iloc[closest_idx]

    # === Metrics ===
    abs_error = abs(y_pred - y_true)
    percent_error = (abs_error / y_true) * 100 if y_true != 0 else None

    # Load existing results if available
    if os.path.exists(EVAL_PATH):
        eval_df = pd.read_csv(EVAL_PATH)
        y_preds = eval_df["Predicted"]
        y_trues = eval_df["Actual"]
    else:
        eval_df = pd.DataFrame(columns=["Predicted", "Actual", "AbsoluteError", "PercentError", "MAE", "RMSE", "R2"])
        y_preds, y_trues = [], []

    # === Update Cumulative Metrics ===
    y_preds = list(y_preds) + [y_pred]
    y_trues = list(y_trues) + [y_true]

    # === Append to CSV ===
    row = {
        "Predicted": round(y_pred, 2),
        "Actual": round(y_true, 2),
        "AbsoluteError": round(abs_error, 2),
        "PercentError": round(percent_error, 2) if percent_error else "N/A"

    }

    pd.DataFrame([row]).to_csv(EVAL_PATH, mode="a", header=False, index=False)

    data = pd.read_csv(EVAL_PATH)
    return data.to_json()

    # === Print ===
    print("\n===== Evaluation of New Claim =====")
    print(f"Predicted Value       : {y_pred:.2f}")
    print(f"Closest Actual Value  : {y_true:.2f}")
    print(f"Absolute Error        : {abs_error:.2f}")
    print(f"Percent Error         : {percent_error:.2f}%")
