import os
from youtube_transcript_api import YouTubeTranscriptApi
from openai import OpenAI
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)


class YTFunctions:
    @staticmethod
    def summarize_video(video_url):
        # Obter a chave de API de uma variável de ambiente
        client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        # Extrair video_id da URL
        if 'watch?v=' in video_url:
            video_id = video_url.split('watch?v=')[-1]
        elif 'youtu.be/' in video_url:
            video_id = video_url.split('youtu.be/')[-1]
        else:
            resumo = "URL do YouTube inválida."
            timecodes = "N/A"
            return resumo, timecodes

        # Obter transcrição
        try:
            from youtube_transcript_api import YouTubeTranscriptApi, TranscriptsDisabled, NoTranscriptFound

            transcript_list = YouTubeTranscriptApi.list_transcripts(video_id)

            # Exibir os idiomas disponíveis
            available_languages = [t.language_code for t in transcript_list]
            print(f"Idiomas disponíveis: {available_languages}")

            # Tentar obter a transcrição em português ou inglês
            try:
                transcript = transcript_list.find_transcript(['pt', 'pt-BR', 'en']).fetch()
            except NoTranscriptFound:
                # Tentar obter a transcrição gerada automaticamente
                transcript = transcript_list.find_generated_transcript(['pt', 'pt-BR', 'en']).fetch()

            # Combinar as partes da transcrição
            transcript_text = " ".join([t['text'] for t in transcript])

        except TranscriptsDisabled:
            print("Transcrições estão desativadas para este vídeo.")
            resumo = "Transcrições estão desativadas para este vídeo."
            timecodes = "N/A"
            return resumo, timecodes
        except NoTranscriptFound:
            print("Nenhuma transcrição foi encontrada para este vídeo.")
            resumo = "Nenhuma transcrição foi encontrada para este vídeo."
            timecodes = "N/A"
            return resumo, timecodes
        except Exception as e:
            print(f"Erro ao obter transcrição: {e}")
            resumo = "Não foi possível obter a transcrição do vídeo."
            timecodes = "N/A"
            return resumo, timecodes

        # Inicializar timecodes
        timecodes = "Funcionalidade de timecodes não implementada."

        # Função para dividir o texto em chunks
        def split_text(text, max_tokens=2048):
            words = text.split()
            chunks = []
            current_chunk = []
            current_length = 0

            for word in words:
                current_chunk.append(word)
                current_length += 1  # Aproximação: 1 palavra = 1 token

                if current_length >= max_tokens:
                    chunks.append(' '.join(current_chunk))
                    current_chunk = []
                    current_length = 0

            if current_chunk:
                chunks.append(' '.join(current_chunk))

            return chunks

        # Dividir a transcrição se necessário
        chunks = split_text(transcript_text, max_tokens=2048)

        resumos = []
        for chunk in chunks:
            try:
                response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {"role": "system", "content": "Você é um assistente educacional que resume vídeos do YouTube."},
                        {"role": "user", "content": f"Resuma o seguinte conteúdo:\n{chunk}"}
                    ],
                    top_p=0.9,
                    temperature=0.8
                )
                resumo_chunk = response.choices[0].message.content.strip()
                resumos.append(resumo_chunk)
            except Exception as e:
                print(f"Erro ao gerar resumo: {e}")
                resumos.append("Não foi possível gerar o resumo para este trecho.")

        # Combinar os resumos dos chunks
        resumo = "\n\n".join(resumos)

        # Retornar o resumo e os timecodes
        return resumo, timecodes

