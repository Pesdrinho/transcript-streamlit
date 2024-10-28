import os
import streamlit as st
from Functions import (
    audio_transcription_service,
    combine_transcriptions,
    extract_audio,
    generate_summary,
    segment_audio,
    transcribe_audio_segments,
    YTFunctions
)

def main():
    st.title("Plataforma de Transcrição e Sumarização")

    # Menu na barra lateral
    menu = ["Transcrever Arquivo", "Resumir Vídeo do YouTube"]
    choice = st.sidebar.selectbox("Selecione uma opção", menu)

    if choice == "Transcrever Arquivo":
        st.header("Transcrição e Sumarização de Arquivo de Áudio/Vídeo")

        uploaded_file = st.file_uploader("Escolha um arquivo de áudio ou vídeo", type=["mp3", "wav", "aac", "flac", "ogg", "mp4", "avi", "mkv", "mov", "wmv"])

        if uploaded_file is not None:
            if st.button("Processar Arquivo"):
                st.info("Processando o arquivo, isso pode levar alguns minutos...")

                # Cria o diretório 'data' se não existir
                if not os.path.exists("data"):
                    os.makedirs("data")

                # Salva o arquivo carregado na pasta 'data'
                uploaded_file_path = os.path.join("data", uploaded_file.name)
                with open(uploaded_file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                # Determina se o arquivo é de áudio ou vídeo com base na extensão
                file_extension = os.path.splitext(uploaded_file.name)[1].lower()

                video_extensions = ['.mp4', '.avi', '.mkv', '.mov', '.wmv']
                audio_extensions = ['.mp3', '.wav', '.aac', '.flac', '.ogg']

                if file_extension in video_extensions:
                    # Se for um vídeo, extrai o áudio e salva na pasta 'data'
                    audio_file = extract_audio(
                        uploaded_file_path,
                        output_audio_path=os.path.join("data", "extracted_audio.wav")
                    )
                    if audio_file is None:
                        st.error("Falha ao extrair o áudio do vídeo.")
                        return
                elif file_extension in audio_extensions:
                    # Se for um áudio, usa o arquivo carregado diretamente
                    audio_file = uploaded_file_path
                else:
                    st.error("Formato de arquivo não suportado.")
                    return

                # Verificar se audio_file não é None
                if audio_file is None:
                    st.error("Erro ao processar o arquivo de áudio.")
                    return

                # Segmentar áudio
                segments = segment_audio(audio_file)
                if not segments:
                    st.error("Falha ao segmentar o arquivo de áudio.")
                    return

                # Transcrever segmentos de áudio
                transcriptions = transcribe_audio_segments(segments)
                if not transcriptions:
                    st.error("Falha ao transcrever os segmentos de áudio.")
                    return

                # Combinar transcrições
                full_transcription = combine_transcriptions(transcriptions)

                # Gerar sumário
                summary = generate_summary(full_transcription)

                # Exibir resultados
                st.subheader("Transcrição")
                st.write(full_transcription)

                st.subheader("Sumarização")
                st.write(summary)

    elif choice == "Resumir Vídeo do YouTube":
        st.header("Resumir Vídeo do YouTube")

        video_url = st.text_input("Insira a URL do vídeo do YouTube")

        if st.button("Resumir Vídeo"):
            if video_url:
                st.info("Processando o vídeo, isso pode levar alguns minutos...")

                # Chamar a função para resumir o vídeo do YouTube
                resumo, timecodes = YTFunctions.summarize_video(video_url)

                if resumo:
                    # Exibir os resultados
                    st.subheader("Resumo")
                    st.write(resumo)

                    st.subheader("Tópicos e Timecodes")
                    st.write(timecodes)
                else:
                    st.error("Não foi possível resumir o vídeo. Verifique a URL e tente novamente.")
            else:
                st.error("Por favor, insira uma URL válida do YouTube.")

if __name__ == "__main__":
    main()