import streamlit as st
from tempfile import NamedTemporaryFile
import whisper
import os

model = whisper.load_model("base")
language = st.selectbox("Select Language", ["English", "Spanish"], index=1)


def get_download_path():
    """Returns the default downloads path for Linux or Windows"""
    if os.name == 'nt':
        import winreg
        sub_key = r'SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders'
        downloads_guid = '{374DE290-123F-4565-9164-39C4925E467B}'
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, sub_key) as key:
                location = winreg.QueryValueEx(key, downloads_guid)[0]
            return location
        except WindowsError:
            pass

    # Fallback for Linux or when Windows registry key is not found
    possible_dirs = ["Downloads", "Descargas"]
    home_dir = os.path.expanduser('~')
    for dir_name in possible_dirs:
        dir_path = os.path.join(home_dir, dir_name)
        if os.path.exists(dir_path):
            return dir_path

    return home_dir


def save_text_as_file(text, audio_filename):
    default_dir = get_download_path()
    save_location = os.path.join(default_dir, audio_filename.replace(".mp3", ".txt"))
    st.write(f"save_location: {save_location}")

    def save_file():
        location_label = "Saving text to" if language == "English" else "Guardando texto en"
        st.write(f"{location_label} {save_location}")
        try:
            with open(save_location, "w") as file:
                file.write(text)
            saved_in_label = "Text saved to" if language == "English" else "Texto guardado en"
            st.success(f"{saved_in_label} {save_location}")
        except Exception as e:
            saved_error_label = "Error saving file" if language == "English" else "Error guardando el archivo"
            st.error(f"{saved_error_label}: {e}")

    save_button_label = "Save" if language == "English" else "Guardar"
    st.button(save_button_label, on_click=save_file)


def main():
    transcribe_button_label = "Transcribe Audio" if language == "English" else "Transcribir Audio"
    title = "Audios transcription" if language == "English" else "Transcripción de Audios"

    st.title(title)

    file_upload_label = "Upload an MP3 file" if language == "English" else "Subir un archivo MP3"
    audio_file = st.file_uploader(file_upload_label, type=["mp3"])

    if audio_file is not None:
        transcribe_button = st.button(transcribe_button_label)
        # Create a temporary file to save the uploaded MP3
        with NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
            temp_file.write(audio_file.read())
            temp_file.flush()

            # Play the uploaded MP3 using playsound library
            st.audio(temp_file.name, format='audio/mp3', start_time=0)
            if  transcribe_button:
                transcribe_spinner_label = "Transcribing audio..." if language == "English" else "Transcribiendo audio..."
                with st.spinner(transcribe_spinner_label):
                    # Transcribe the uploaded MP3
                    result = model.transcribe(temp_file.name)
                    if result:
                        transcription_finished_label = "Transcription completed!" if language == "English" else "Transcripción completada!"
                        st.success(transcription_finished_label)
                        transcription = result["text"]
                        transcription_label = "Transcription" if language == "English" else "Transcripción"
                        help_text = "Here you can modify transcribed text" if language == "English" else "Aquí puedes modificar el texto transcripto"
                        st.text_area(transcription_label, transcription, height=600, help=help_text)
                        save_text_as_file(transcription, audio_file.name)

if __name__ == "__main__":
    main()
