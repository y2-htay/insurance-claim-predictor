import pandas as pd
import matplotlib.pyplot as plt
import time
import os

# === Paths ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EVAL_PATH = os.path.join(BASE_DIR, 'evaluation_results.csv')

def plot_real_time_graph(csv_path, refresh_interval=5):
    """
    Real-time plot of settlement values vs. error from the evaluation_results.csv file.

    Args:
        csv_path (str): Path to the evaluation_results.csv file.
        refresh_interval (int): Time interval (in seconds) to refresh the graph.
    """
    last_modified_time = None

    plt.ion()  # Turn on interactive mode for real-time updates
    fig, ax = plt.subplots(figsize=(8, 6))

    while True:
        # Check if the file has been modified
        current_modified_time = os.path.getmtime(csv_path)
        if last_modified_time is None or current_modified_time != last_modified_time:
            last_modified_time = current_modified_time

            # Read the CSV file
            try:
                eval_df = pd.read_csv(csv_path, names=["Predicted", "Actual", "AbsoluteError", "PercentError"])
            except Exception as e:
                print(f"Error reading CSV file: {e}")
                time.sleep(refresh_interval)
                continue

            # Ensure required columns exist
            if not {"Actual", "AbsoluteError"}.issubset(eval_df.columns):
                print("CSV file does not contain required columns: 'Actual' and 'AbsoluteError'")
                break

            # Extract data for plotting
            settlement_values = eval_df["Actual"]
            absolute_errors = eval_df["AbsoluteError"]

            # Sort the data by Settlement Values
            sorted_indices = settlement_values.argsort()
            settlement_values = settlement_values.iloc[sorted_indices]
            absolute_errors = absolute_errors.iloc[sorted_indices]

            # Clear the previous plot
            ax.clear()

            # Plot the graph
            ax.plot(settlement_values, absolute_errors, marker="o", linestyle="-", color="green", label="Error vs Settlement")
            ax.set_title("Error vs Settlement Value (Real-Time)")
            ax.set_xlabel("Settlement Value")
            ax.set_ylabel("Error")
            ax.legend()
            ax.grid(True)

            # Redraw the plot
            plt.draw()
            plt.pause(0.1)  # Pause to allow the graph to update

        # Wait for the next refresh
        time.sleep(refresh_interval)

# === Run the Real-Time Plot ===
if __name__ == "__main__":
    plot_real_time_graph(EVAL_PATH, refresh_interval=5)