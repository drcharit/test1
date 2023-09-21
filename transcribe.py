import os
import streamlit as st
from google.cloud import speech_v1p1beta1 as speech
from google.cloud.speech_v1p1beta1 import types

# Set up authentication
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "YOUR_JSON_KEY_PATH"

def transcribe_audio(audio_file):
    client = speech.SpeechClient()

    audio_content = audio_file.read()
    audio = types.RecognitionAudio(content=audio_content)
    config = types.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="en-US",
    )

    response = client.recognize(config=config, audio=audio)

    transcript = ""
    for result in response.results:
        transcript += result.alternatives[0].transcript + "\n"

    return transcript

st.title("MP3 Transcription App")
st.write("Upload your MP3 file and then click the 'Transcribe' button to get a transcript.")

uploaded_file = st.file_uploader("Choose an MP3 file", type="mp3")

if uploaded_file:
    if st.button("Transcribe"):
        with st.spinner("Transcribing..."):
            transcript = transcribe_audio(uploaded_file)
        st.text_area("Transcript", transcript, height=300)
