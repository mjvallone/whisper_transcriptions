import streamlit as st
from tempfile import NamedTemporaryFile
import whisper
import os
# from tkinter import filedialog


model = whisper.load_model("base")
language = st.selectbox("Select Language", ["English", "Spanish"], index=1)


def save_text_as_file(text, audio_filename):
    save_directory = st.text_input("Save Directory", "/home/tincho/Documentos")
    save_filename = st.text_input("Save Filename", audio_filename.replace(".mp3", ".txt").strip())
    save_location = os.path.join(save_directory, save_filename)
    #FIXME be able to save it to where you want, not fixed location

    # save_location = st.text_input("Save Location", audio_filename.replace(".mp3", ".txt").strip())
    # if st.button("Choose Directory"):
    #     import pdb; pdb.set_trace()
    #     root = st._root
    #     root.withdraw()
    #     folder_selected = filedialog.askdirectory()
    #     save_location = os.path.join(folder_selected, os.path.basename(save_location))

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
        if  transcribe_button:
            # Create a temporary file to save the uploaded MP3
            with NamedTemporaryFile(suffix=".mp3", delete=False) as temp_file:
                temp_file.write(audio_file.read())
                temp_file.flush()

                # Play the uploaded MP3 using playsound library
                st.audio(temp_file.name, format='audio/mp3', start_time=0)
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
