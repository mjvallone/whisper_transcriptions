import streamlit as st
from tempfile import NamedTemporaryFile
import whisper


model = whisper.load_model("base")
languages = {
    "English": {
        "download_label": "The file *{file_name}* will be downloaded",
        "download_button_label": "Download file (original text)",
        "transcribe_button_label": "Transcribe Audio",
        "title": "Audios transcription",
        "file_upload_label": "Upload an MP3 file",
        "transcribe_spinner_label": "Transcribing audio...",
        "transcription_finished_label": "Transcription completed!",
        "transcription_label": "Transcription",
        "help_text": "Here you can modify transcribed text"
    },
    "Spanish": {
        "download_label": "El archivo *{file_name}* será descargado",
        "download_button_label": "Descargar archivo (texto original)",
        "transcribe_button_label": "Transcribir Audio",
        "title": "Transcripción de Audios",
        "file_upload_label": "Subir un archivo MP3",
        "transcribe_spinner_label": "Transcribiendo audio...",
        "transcription_finished_label": "Transcripción completada!",
        "transcription_label": "Transcripción",
        "help_text": "Aquí puedes modificar el texto transcripto"
    }
}


def save_text_as_file(audio_filename, lang_data):
    file_name = audio_filename.split(".")[0]+".txt"
    st.write(lang_data["download_label"].format(file_name=file_name))

    st.download_button(
        lang_data["download_button_label"], 
        data=st.session_state.transcription, 
        file_name=file_name
    )


def main():
    selected_language = st.selectbox("Select Language", ["English", "Spanish"], index=1)
    lang_data = languages[selected_language]

    st.title(lang_data["title"])

    audio_file = st.file_uploader(lang_data["file_upload_label"], type=["mp3"])

    if audio_file is not None:
        transcribe_button = st.button(lang_data["transcribe_button_label"])
        # Create a temporary file to save the uploaded MP3
        with NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
            temp_file.write(audio_file.read())
            temp_file.flush()

            # Play the uploaded MP3 using playsound library
            st.audio(temp_file.name, format='audio/mp3', start_time=0)

            if  transcribe_button:
                with st.spinner(lang_data["transcribe_spinner_label"]):
                    # Transcribe the uploaded MP3
                    result = model.transcribe(temp_file.name)
                    if result:
                        st.success(lang_data["transcription_finished_label"])
                        st.text_area(
                            label=lang_data["transcription_label"], 
                            height=600, 
                            help=lang_data["help_text"],
                            key='transcription',
                            value=result["text"]
                        )
                        save_text_as_file(audio_file.name, lang_data)


if __name__ == "__main__":
    main()
