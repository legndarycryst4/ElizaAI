import os
from llama_cpp import Llama
import subprocess

# Load Llama model
from .credentials import LLAMA_MODEL_PATH
llama = Llama(model_path=LLAMA_MODEL_PATH)

def generate_text_by_audio(audio_filename="audio.mp3"):
    dir_path = os.environ["BASE_DIR_PATH"]
    audio_file_path = f"{dir_path}/{audio_filename}"

    # Transcribe audio using Whisper.cpp
    transcription_cmd = f'whisper.cpp/main -m whisper/models/ggml-large.bin -f "{audio_file_path}"'
    transcription_result = subprocess.run(transcription_cmd, shell=True, capture_output=True, text=True)
    transcription_text = transcription_result.stdout.strip()

    # Generate response using Llama
    response = llama(transcription_text)
    print("Transcription = " + transcription_text)
    print("Llama Response = " + response["choices"][0]["text"].strip())
