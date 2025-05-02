import pandas as pd
import os

def create_detailed_errors_csv(folder, prediction_file):
    try:
        print(f"🔍 Creating detailed error report for {folder}...")

        # Load prediction file
        path = os.path.join(folder, prediction_file)
        df = pd.read_csv(path)

        # Rename columns if needed
        actual_col = [col for col in df.columns if 'actual' in col.lower()][0]
        predicted_col = [col for col in df.columns if 'predict' in col.lower()][0]

        # Calculate error columns
        df["Absolute Error"] = (abs(df[actual_col] - df[predicted_col])).round(3)
        df["Percentage Error"] = ((df["Absolute Error"] / df[actual_col].abs()) * 100).round(3)

        from sklearn.metrics import r2_score, mean_squared_error

        # Calculate global metrics
        r2 = r2_score(df[actual_col], df[predicted_col])
        rmse = mean_squared_error(df[actual_col], df[predicted_col], squared=False)

        # Add as constant columns
        df["R²"] = round(r2, 3)
        df["RMSE"] = round(rmse, 3)


        # Save as new CSV
        output_file = os.path.join(folder, "detailed_errors.csv")
        df[[actual_col, predicted_col, "Absolute Error", "Percentage Error", "R²", "RMSE"]].to_csv(output_file, index=False)


        print(f"✅ detailed_errors.csv saved in {folder}\n")

    except Exception as e:
        print(f"❌ Error processing {folder}: {e}")


create_detailed_errors_csv(".", "predictions.csv")

