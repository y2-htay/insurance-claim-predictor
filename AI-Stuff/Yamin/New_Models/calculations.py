import pandas as pd
import os
from sklearn.metrics import r2_score, mean_squared_error

def detailed_errors_current_folder(file_name):
    try:
        print(f"🔍 Generating detailed errors for {file_name}...")

        df = pd.read_csv(file_name)

        actual_col = "Actual"
        models = ["RandomForest_Predicted", "Stacking_Predicted"]

        for model_col in models:
            # Error metrics
            abs_err_col = f"{model_col}_AbsError"
            pct_err_col = f"{model_col}_PctError"
            df[abs_err_col] = (abs(df[actual_col] - df[model_col])).round(3)
            df[pct_err_col] = ((df[abs_err_col] / df[actual_col].abs()) * 100).round(3)

            # Global scores
            r2 = r2_score(df[actual_col], df[model_col])
            rmse = mean_squared_error(df[actual_col], df[model_col], squared=False)

            # Constant columns
            df[f"{model_col}_R2"] = round(r2, 3)
            df[f"{model_col}_RMSE"] = round(rmse, 3)

        # Save
        output_file = "detailed_errors.csv"
        df.to_csv(output_file, index=False)

        print(f"✅ detailed_errors.csv saved with R² and RMSE.\n")

    except Exception as e:
        print(f"❌ Failed to process: {e}")

# Run it
detailed_errors_current_folder("model_predictions.csv")
