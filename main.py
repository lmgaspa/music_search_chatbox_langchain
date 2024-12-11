import streamlit as st
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os

# Carregar variáveis de ambiente
load_dotenv()

# Obter as chaves da API do .env
YOUTUBE_API_KEY = os.getenv("API_KEY")  # Certifique-se de que o .env tem a variável API_KEY

# Verificar se a chave foi carregada
if not YOUTUBE_API_KEY:
    st.error("API_KEY não foi carregada. Verifique o arquivo .env e a configuração do código.")
    raise SystemExit("API_KEY não encontrada no .env. Encerrando o programa.")

# Função para buscar músicas no YouTube
def search_music_youtube(query, max_results=5):
    """
    Busca músicas no YouTube com base na consulta do usuário.
    """
    try:
        youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)
        search_response = youtube.search().list(
            q=query,
            part="snippet",
            maxResults=max_results,
            type="video"
        ).execute()

        music_results = []
        for item in search_response.get("items", []):
            music_results.append({
                "title": item["snippet"]["title"],
                "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                "channel": item["snippet"]["channelTitle"]
            })
        return music_results

    except Exception as e:
        raise RuntimeError(f"Erro ao buscar no YouTube: {e}")

# Aplicação com Streamlit
def main():
    st.title("🎵 YouTube Music Searcher")
    st.write("Procure por suas músicas favoritas diretamente no YouTube!")

    # Entrada do usuário para busca
    user_input = st.text_input("Digite o nome da música, artista ou gênero:", "")

    if st.button("Buscar"):
        if user_input.strip():
            # Buscar músicas no YouTube
            try:
                results = search_music_youtube(user_input)
                if results:
                    st.write(f"### Resultados da busca por: {user_input}")
                    for idx, music in enumerate(results, 1):
                        st.write(f"**{idx}. {music['title']}**")
                        st.write(f"- **Canal:** {music['channel']}")
                        st.write(f"- [Assistir no YouTube]({music['url']})")
                        st.write("---")
                else:
                    st.warning("Nenhum resultado encontrado. Tente outro termo.")
            except Exception as e:
                st.error(f"Erro ao buscar músicas: {e}")
        else:
            st.warning("Por favor, insira o nome da música, artista ou gênero para buscar.")

if __name__ == "__main__":
    main()
