import streamlit as st
from tempfile import NamedTemporaryFile
import whisper

@st.cache_resource(show_spinner=False)
def load_model():
    return whisper.load_model("base")

model = load_model()
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
        "help_text": "Here you can modify transcribed text",
        "sidebar_line1": "This application is designed for audio transcriptions.",
        "sidebar_line2": "Please upload an MP3 file in any language and click the 'Transcribe audio' button.",
        "sidebar_line3": "After a short processing time (depending on the length of the audio file), the transcription will be displayed.",
        "sidebar_line4": "To verify the accuracy of the transcription, you can play the audio.",
        "sidebar_line5": "You can also download the transcription as a text file by clicking the 'Download file (original text)' button.",
        "sidebar_line6": "If you have multiple audio files to transcribe, you can use the bulk transcription feature. Check out the <a href='https://github.com/mjvallone/whisper_transcriptions'>documentation on GitHub</a> for more information.",
        "sidebar_line7": "This application utilizes the following technologies:",
        "sidebar_line8": "Streamlit - a lightweight open-source app framework for Machine Learning and Data Science projects",
        "sidebar_line9": "Whisper - a library for audio transcription powered by OpenAI",
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
        "help_text": "Aquí puedes modificar el texto transcripto",
        "sidebar_line1": "Esta aplicación está diseñada para transcripciones de audio.",
        "sidebar_line2": "Por favor, sube un archivo MP3 en cualquier idioma y haz clic en el botón 'Transcribir audio'.",
        "sidebar_line3": "Después de un tiempo breve (dependiendo del largo del audio), la transcripción se mostrará.",
        "sidebar_line4": "Para verificar la exactitud de la transcripción, puedes reproducir el audio.",
        "sidebar_line5": "Puedes descargar el archivo de transcripción como un archivo de texto haciendo clic en el botón 'Descargar archivo (texto original)'",
        "sidebar_line6": "Si tienes varios archivos de audio para transcribir, puedes utilizar la función de transcripción masiva. Consulta la <a href='https://github.com/mjvallone/whisper_transcriptions'>documentación en GitHub</a> para obtener más información.",
        "sidebar_line7": "Esta aplicación utiliza las siguientes tecnologías:",
        "sidebar_line8": "Streamlit - una aplicación de escritorio abierta para proyectos de Machine Learning y Data Science",
        "sidebar_line9": "Whisper - una biblioteca para la transcripción de audio basada en OpenAI",
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
    selected_language = st.selectbox("Seleccionar idioma", ["English", "Spanish"], index=1)
    lang_data = languages[selected_language]

    st.title(lang_data["title"])

    st.sidebar.markdown(f"""
        <!DOCTYPE html>
        <html lang="en">
        <body>
            <p>{lang_data["sidebar_line1"]}</p>
            <p>{lang_data["sidebar_line2"]}</p>
            <p>{lang_data["sidebar_line3"]}</p>
            <p>{lang_data["sidebar_line4"]}</p>
            <p>{lang_data["sidebar_line5"]}</p>
            <br/>
            <p>{lang_data["sidebar_line6"]}</p>
            <p>{lang_data["sidebar_line7"]}</p>
            <ul>
                <li>{lang_data["sidebar_line8"]}</li>
                <li>{lang_data["sidebar_line9"]}</li>
            </ul>
        </body>
        </html>
        """, unsafe_allow_html=True)

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
