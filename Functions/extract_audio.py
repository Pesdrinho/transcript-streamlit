import moviepy.editor as mp

def extract_audio(video_file_path, output_audio_path):
    try:
        video = mp.VideoFileClip(video_file_path)
        video.audio.write_audiofile(output_audio_path)
        return output_audio_path
    except Exception as e:
        print(f"Erro ao extrair áudio: {e}")
        return None