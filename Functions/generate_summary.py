import os
from openai import OpenAI
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

def generate_summary(transcription_text):
    response = client.chat.completions.create(
         model="gpt-4o-mini",
         messages=[
                {"role": "system", "content": "Você é um assistente educacional, por favor faça um resumo dos videos do usuario."},
                {"role": "user", "content": f"Desenvolva um resumo bem estruturado e que abranja todos os tópicos apresentados na transcrição do vídeo a seguir: {transcription_text}"}
            ],
         top_p = 0.9,
         temperature = 0.9
      )
    
    summary = response.choices[0].message.content
    return summary