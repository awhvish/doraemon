import pandas as pd
import matplotlib.pyplot as plt
import os

# Define paths
data_path = "/home/awhvish/Downloads/cognitive-overload-detection/data/blinks_movements.csv"
output_dir = "/home/awhvish/Downloads/cognitive-overload-detection/output"
output_graph = os.path.join(output_dir, "cognitive_load_graph.png")

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

try:
    # Ensure the data file exists
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"File not found at {data_path}")
    
    # Load CSV file
    df = pd.read_csv(data_path)

    # Validate required columns
    required_columns = {"Time Interval", "Blinks", "Eye Movements"}
    if not required_columns.issubset(df.columns):
        raise ValueError(f"Missing required columns. Expected: {required_columns}, Found: {set(df.columns)}")
    
    # Drop any rows with missing values in required columns
    df = df.dropna(subset=["Time Interval", "Blinks", "Eye Movements"])
    
    # Convert timestamp to string if needed
    df["Time Interval"] = df["Time Interval"].astype(str)
    
    # Compute cognitive load as a weighted sum of blinks and eye movements
    alpha = 0.7
    beta = 0.3
    df["cognitive_load"] = alpha * df["Blinks"] + beta * df["Eye Movements"]

    # Plot the graph
    plt.figure(figsize=(12, 6))
    plt.plot(df["Time Interval"], df["cognitive_load"], marker='o', linestyle='-', label="Cognitive Load")
    plt.axhline(y=0.6, color="r", linestyle="--", label="Overload Threshold")
    plt.xlabel("Time Interval")
    plt.ylabel("Cognitive Load")
    plt.title("Cognitive Load Over Time")
    plt.xticks(rotation=45)
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    
    # Save graph
    plt.savefig(output_graph)
    plt.close()
    print(f"✅ Graph saved at: {output_graph}")

except FileNotFoundError as e:
    print(f"❌ Error: {e}")

except pd.errors.EmptyDataError:
    print("❌ Error: The CSV file is empty.")