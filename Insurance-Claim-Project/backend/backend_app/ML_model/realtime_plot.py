import pandas as pd
import matplotlib.pyplot as plt
import time
import os

# === Paths ===
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
EVAL_PATH = os.path.join(BASE_DIR, 'evaluation_results.csv')
GRAPH_PATH = os.path.join(BASE_DIR, 'realtime_graph.png')  # Path to save the graph

def plot_real_time_graph(csv_path, graph_path, refresh_interval=5):
    """
    Real-time plot of settlement values vs. error from the evaluation_results.csv file.

    Args:
        csv_path (str): Path to the evaluation_results.csv file.
        graph_path (str): Path to save the generated graph image.
        refresh_interval (int): Time interval (in seconds) to refresh the graph.
    """
    last_modified_time = None

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

            # Create the plot
            plt.figure(figsize=(8, 6))
            plt.plot(settlement_values, absolute_errors, marker="o", linestyle="-", color="green", label="Error vs Settlement")
            plt.title("Error vs Settlement Value (Real-Time)")
            plt.xlabel("Settlement Value")
            plt.ylabel("Error")
            plt.legend()
            plt.grid(True)

            # Save the plot as an image
            plt.savefig(graph_path)
            plt.close()  # Close the plot to free memory

        # Wait for the next refresh
        time.sleep(refresh_interval)

# === Run the Real-Time Plot ===
if __name__ == "__main__":
    plot_real_time_graph(EVAL_PATH, GRAPH_PATH, refresh_interval=5)