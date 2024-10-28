from Functions import (
    combine_transcriptions,
    extract_audio,
    segment_audio,
    transcribe_audio_segments
)

def audio_transcription_service(video_path):
    # Extraindo o áudio do vídeo
    audio_path = "temp_audio.wav"
    extract_audio(video_path, audio_path)

    # Segmentando o áudio em intervalos de silêncio
    segments = segment_audio(audio_path)

    # Transcrevendo cada segmento e combinando os textos
    transcriptions = transcribe_audio_segments(segments)
    full_text = combine_transcriptions(transcriptions)

    return full_text