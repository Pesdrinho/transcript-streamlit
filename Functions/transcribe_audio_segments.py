import os

from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

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