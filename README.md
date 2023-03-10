# Whisper transcriptions
The main idea here is to create a tool to transcript audios to text by using Whisper (speech to text from OpenAI)

## It doesn't matter how you are going to transcript, first you should do this

1. You should install python3.8 :)

2. on Ubuntu or Debian:

        sudo apt update && sudo apt install ffmpeg

## Then to run it

1. Create virtualenv using python3 (follow https://virtualenvwrapper.readthedocs.io/en/latest/install.html)

        virtualenv venv -p python3.8

2. Activate the virtualenv

        source env/bin/activate

3. Install python requirements (be patient, it takes time)

        pip install -r requirements.txt

## If you want to run script for bulk transcription
Run 

        python transcript_automation.py PATH_TO_FOLDER_WITH_MP3s

For every mp3 file you'll get a text file with audio transcription in the same folder where audio is. Text file will be name as the audio file.

## If you want to run it with Streamlit (Work In Progress)

4. Run main.py with streamlit and get a transcription!

        streamlit run main.py
