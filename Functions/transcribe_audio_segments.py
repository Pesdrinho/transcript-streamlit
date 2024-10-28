import os

from openai import OpenAI
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def transcribe_audio_segments(segments):
    transcriptions = []
    for i, segment in enumerate(segments):
        segment.export(f"segment_{i}.wav", format="wav")
        with open(f"segment_{i}.wav", "rb") as audio_file:
            transcript = client.audio.transcriptions.create(
            model="whisper-1", 
            file=audio_file
            )
            transcriptions.append(transcript.text)
    return transcriptions