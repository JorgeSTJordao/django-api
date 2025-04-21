import os
from googleapiclient.discovery import build
from dotenv import load_dotenv
from datetime import datetime

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

def search_youtube_videos(query, max_results=10):
    """
    Busca vídeos no YouTube usando a API V3.
    
    Args:
        query (str): Termo de busca
        max_results (int): Número máximo de resultados (padrão: 10)
    
    Returns:
        list: Lista de vídeos encontrados
    """
    # Obtém a chave da API do arquivo .env
    api_key = os.getenv('YOUTUBE_API_KEY')
    
    if not api_key:
        raise ValueError("Chave da API do YouTube não encontrada. Verifique o arquivo .env")
    
    # Inicializa o serviço da API do YouTube
    youtube = build('youtube', 'v3', developerKey=api_key)
    
    # Faz a requisição de busca
    request = youtube.search().list(
        part='snippet',
        q=query,
        type='video',
        order='date',
        maxResults=max_results
    )
    
    response = request.execute()
    
    # Processa os resultados
    videos = []
    for item in response.get('items', []):
        video = {
            'title': item['snippet']['title'],
            'video_id': item['id']['videoId'],
            'published_at': item['snippet']['publishedAt'],
            'channel_title': item['snippet']['channelTitle'],
            'description': item['snippet']['description'],
            'thumbnail_url': item['snippet']['thumbnails']['default']['url']
        }
        videos.append(video)
    
    return videos

def main():
    # Exemplo de uso
    game_name = "Minecraft"  # Você pode alterar para o jogo desejado
    try:
        videos = search_youtube_videos(game_name)
        
        print(f"\nVídeos mais recentes sobre {game_name}:")
        print("-" * 50)
        
        for video in videos:
            published_date = datetime.strptime(video['published_at'], '%Y-%m-%dT%H:%M:%SZ')
            print(f"\nTítulo: {video['title']}")
            print(f"Canal: {video['channel_title']}")
            print(f"Publicado em: {published_date.strftime('%d/%m/%Y %H:%M')}")
            print(f"Link: https://www.youtube.com/watch?v={video['video_id']}")
            print("-" * 50)
            
    except Exception as e:
        print(f"Erro ao buscar vídeos: {str(e)}")

if __name__ == "__main__":
    main()
