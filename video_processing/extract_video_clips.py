import os
import subprocess
import sys

# Get the absolute path of the current script
base_path = os.path.dirname(os.path.abspath(__file__))

# Construct correct paths
timestamps_file = os.path.join(base_path, "../output/timestamps.txt")
input_video = os.path.join(base_path, "../data/input_video.mp4")
output_dir = os.path.join(base_path, "../output/video_clips")

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

try:
    # Read timestamps
    with open(timestamps_file, "r") as f:
        timestamps = [float(line.strip()) for line in f.readlines()]

    if not timestamps:
        print("❌ No timestamps found!")
        sys.exit(1)

    # Process video clips using FFmpeg
    for i, ts in enumerate(timestamps):
        start_time = max(0, ts - 30)  # ±5 min (300 sec total)
        duration = 60  # 5 minutes

        # Ensure unique filenames by appending timestamp
        output_clip = os.path.join(output_dir, f"clip_{i}_{int(ts)}.mp4")

        ffmpeg_cmd = [
            "ffmpeg", "-y",  # Overwrite existing files without prompt
            "-i", input_video,
            "-ss", str(start_time),
            "-t", str(duration),  # Correct way to specify duration
            "-c", "copy",  # Copy streams without re-encoding
            output_clip
        ]

        print(f"📌 Extracting: {output_clip} (Start: {start_time}s, Duration: {duration}s)")
        subprocess.run(ffmpeg_cmd, check=True)

    print("✅ Extracted all video clips successfully!")

except FileNotFoundError:
    print(f"❌ Error: {timestamps_file} or {input_video} not found!")

except subprocess.CalledProcessError as e:
    print(f"❌ FFmpeg Error: {e}")

except Exception as e:
    print(f"❌ Unexpected Error: {e}")
