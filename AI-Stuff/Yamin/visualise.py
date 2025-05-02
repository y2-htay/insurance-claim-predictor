import os
import pandas as pd
import matplotlib.pyplot as plt

def generate_prediction_plot(folder, file_name):
    try:
        path = os.path.join(folder, file_name)
        df = pd.read_csv(path)

        # Auto-detect actual and predicted columns
        actual_col = [col for col in df.columns if "actual" in col.lower()][0]
        predicted_col = [col for col in df.columns if "predict" in col.lower()][0]

        actual = df[actual_col]
        predicted = df[predicted_col]

        # Create plot
        plt.figure(figsize=(7, 5))
        plt.scatter(actual, predicted, alpha=0.6, color="mediumseagreen", edgecolors='k', s=25)
        plt.plot([actual.min(), actual.max()], [actual.min(), actual.max()], 'r--', lw=2)

        plt.xlabel("Actual Settlement Value")
        plt.ylabel("Predicted Settlement Value")
        plt.title(f"Actual vs Predicted: {folder.replace('_', ' ')}")
        plt.tight_layout()

        # Save plot
        plot_path = os.path.join(folder, "prediction_plot.png")
        plt.savefig(plot_path)
        plt.close()

        print(f"✅ Plot saved: {plot_path}\n")

    except Exception as e:
        print(f"❌ Failed to create plot for {folder}: {e}")

# === Run on selected folders ===
folders = ["Base_model", "New_Models", "Stacking_model"]

for folder in folders:
    # Look for a file with "prediction" in name
    try:
        files = os.listdir(folder)
        prediction_file = next(f for f in files if "prediction" in f.lower() and f.endswith(".csv"))
        generate_prediction_plot(folder, prediction_file)
    except StopIteration:
        print(f"⚠️  No prediction CSV found in {folder}\n")
    except Exception as e:
        print(f"❌ Error in folder {folder}: {e}")
