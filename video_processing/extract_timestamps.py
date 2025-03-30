import pandas as pd
import os

# Ensure script looks for the file inside the correct project directory
script_dir = os.path.dirname(os.path.abspath(__file__))  # Get script directory
data_path = os.path.join(script_dir, "../data/blinks_movements.csv") 
output_path = os.path.join(script_dir, "../output/timestamps.txt")

print(f"📌 Using Data Path: {data_path}")

# Load data
try:
    df = pd.read_csv(data_path)

    # Ensure the required columns exist
    if "timestamp" not in df.columns or "cognitive_load" not in df.columns:
        raise ValueError("❌ Error: Missing required columns 'timestamp' or 'cognitive_load' in CSV file!")

    overload_timestamps = df[df["cognitive_load"] > 0.6]["timestamp"]

    # Save overload timestamps to a file
    os.makedirs(os.path.join(script_dir, "../output"), exist_ok=True)
    with open(output_path, "w") as f:
        for ts in overload_timestamps:
            f.write(str(ts) + "\n")

    print(f"✅ Overload timestamps saved to {output_path}")

except FileNotFoundError:
    print(f"❌ Error: {data_path} not found!")
except ValueError as ve:
    print(str(ve))
