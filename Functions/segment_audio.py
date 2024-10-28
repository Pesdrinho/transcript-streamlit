from pydub import AudioSegment
from pydub.silence import split_on_silence
import os

def segment_audio(audio_path, min_silence_len=50, silence_thresh=-40, max_segment_len=30000):
    # Determinar o formato do arquivo com base na extensão
    file_extension = os.path.splitext(audio_path)[1].lower()
    if file_extension.startswith('.'):
        file_extension = file_extension[1:]  # Remover o ponto

    # Verificar se o arquivo existe
    if not os.path.isfile(audio_path):
        print(f"Arquivo de áudio não encontrado: {audio_path}")
        return []

    # Carregar o arquivo de áudio usando o formato apropriado
    try:
        audio = AudioSegment.from_file(audio_path, format=file_extension)
    except Exception as e:
        print(f"Erro ao carregar o arquivo de áudio: {e}")
        return []

    # Dividir o áudio em segmentos com base no silêncio
    segments = split_on_silence(
        audio,
        min_silence_len=min_silence_len,
        silence_thresh=silence_thresh,
        keep_silence=15
    )
    
    final_segments = []
    current_segment = AudioSegment.empty()
    
    for segment in segments:
        if len(current_segment) + len(segment) > max_segment_len:
            final_segments.append(current_segment)
            current_segment = AudioSegment.empty()
        current_segment += segment
    
    if len(current_segment) > 0:
        final_segments.append(current_segment)
 
    return final_segments
