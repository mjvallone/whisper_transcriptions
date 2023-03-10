import os
import sys
import glob
import whisper

model = whisper.load_model("base")

if len(sys.argv) < 2:
    print("Usage: python list_files.py <folder_name>")
    sys.exit(1)

folder_name = sys.argv[1]
if not os.path.isdir(folder_name):
    print(f"{folder_name} is not a valid directory")
    sys.exit(1)

mp3_files = glob.glob(os.path.join(folder_name, "*.mp3"))

if not mp3_files:
    print(f"No MP3 files found in {folder_name}")
    sys.exit(1)

print(f"Found {len(mp3_files)} MP3 files in {folder_name}:")

for mp3_file in mp3_files:
    transcription_filename = os.path.splitext(mp3_file)[0] + '.txt'
    print(f"Processing file: {mp3_file}")
    result = model.transcribe(mp3_file)
    with open(transcription_filename, "w") as f:
      f.write(result["text"])
      print(f"Audio transcription ended. Result is saved in file: {transcription_filename}")

