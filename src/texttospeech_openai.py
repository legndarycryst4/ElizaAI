from .generate_audio import play_audio
import requests
from .credentials import ELEVENLABS_APIKEY, ELEVENLABS_VOICEID

def generate_audio_and_subtitle(
    user_question: str, bot_response: str, audio_filename="audio.mp3"
):
    text_to_transform_to_audio = user_question + "? " + bot_response
    
    response = requests.post(
        f"https://api.elevenlabs.io/v1/text-to-speech/{ELEVENLABS_VOICEID}",
        json={"text": text_to_transform_to_audio},
        headers={"xi-api-key": ELEVENLABS_APIKEY, "Content-Type": "application/json"},
    )

    with open(audio_filename, "wb") as f:
        f.write(response.content)
    play_audio(audio_filename)
