import streamlit as st
from audio_recorder_streamlit import audio_recorder
# export OPENAI_API_KEY=
import time

from openai import OpenAI
client = OpenAI()

def convert_input_audio_to_text(inp_file):
    inp_file= open("input_audio.mp3", "rb")
    transcription = client.audio.transcriptions.create(
      model="whisper-1",
      file=inp_file
    )
    print(transcription.text)
    return transcription.text


def get_llm_response(transcription_text):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": transcription_text},
        ]
    )
    llm_response_message = response.choices[0].message.content
    print(llm_response_message)
    return llm_response_message

def convert_llm_response_to_audio(llm_response_message):
    speech_file_path = "output_speech.mp3"
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=llm_response_message
    )

    response.stream_to_file(speech_file_path)
    st.audio(speech_file_path, format="audio/mp3")

# https://pypi.org/project/audio-recorder-streamlit/

audio_bytes = audio_recorder()
if audio_bytes:
    inp_file = open("input_audio.mp3", "wb")
    inp_file.write(audio_bytes)
    tic = time.perf_counter()
    transcription_text = convert_input_audio_to_text(inp_file)
    toc = time.perf_counter()
    elapsed_time = toc - tic
    st.write(f"converted input audio to text in time {elapsed_time} seconds")
    tic = time.perf_counter()
    llm_response_message = get_llm_response(transcription_text)
    toc = time.perf_counter()
    elapsed_time = toc - tic
    st.write(f"got llm response in time {elapsed_time} seconds")
    tic = time.perf_counter()
    convert_llm_response_to_audio(llm_response_message)
    toc = time.perf_counter()
    st.write(f"converted llm response to audio in time {elapsed_time} seconds")
