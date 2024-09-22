import streamlit as st
import openai
import os
import tempfile

# Set your OpenAI API key here or use environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")  # Ensure you set this in your environment

def translate_text(text, target_language):
    # Call the OpenAI API for translation
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f"Translate the following text to {target_language}: {text}"}
        ]
    )
    return response['choices'][0]['message']['content']

def transcribe_audio(file):
    # Transcribe audio to text using OpenAI's Whisper model
    transcription = openai.Audio.transcribe(
        model="whisper-1",
        file=file,
        response_format="text"
    )
    return transcription['text']  # Accessing the 'text' key correctly

def text_to_speech(text):
    # Generate speech from text using OpenAI's TTS model (if available)
    response = openai.Audio.create(
        model="text-to-speech",  # Update with the correct TTS model if available
        input=text,
        voice="alloy"  # Specify voice as needed
    )
    
    # Save audio to a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as temp_file:
        temp_file.write(response['audio'])  # Update according to actual response structure
        return temp_file.name

# Streamlit app layout
st.title("Multilingual Translator")
st.write("Enter text to translate or upload audio:")

# Input text area
input_text = st.text_area("Text to Translate", height=150)

# Upload audio file
uploaded_file = st.file_uploader("Upload MP3 File", type=["mp3"])

# Target language selection
target_language = st.selectbox("Select Target Language", ["Spanish", "French", "German", "Chinese", "Japanese"])

if st.button("Translate"):
    if input_text:
        translated_text = translate_text(input_text, target_language)
        st.subheader("Translated Text:")
        st.write(translated_text)
        
        # Convert translated text to speech and provide playback option
        audio_file_path = text_to_speech(translated_text)
        st.audio(audio_file_path)

    elif uploaded_file:
        # Transcribe and translate uploaded audio file
        transcribed_text = transcribe_audio(uploaded_file)  # Directly pass the uploaded file object
        st.subheader("Transcribed Text:")
        st.write(transcribed_text)

        translated_audio_text = translate_text(transcribed_text, target_language)
        st.subheader("Translated Audio Text:")
        st.write(translated_audio_text)
        
        # Convert translated text to speech and provide playback option
        audio_file_path = text_to_speech(translated_audio_text)
        st.audio(audio_file_path)

    else:
        st.error("Please enter text or upload an audio file to translate.")