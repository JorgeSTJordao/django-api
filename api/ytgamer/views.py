from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .serializers import YouTubeVideoSerializer
from googleapiclient.discovery import build
import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente
load_dotenv()

class YouTubeViewSet(viewsets.ViewSet):
    """
    ViewSet para buscar vídeos do YouTube.
    """
    
    def get_youtube_service(self):
        """Inicializa o serviço da API do YouTube."""
        api_key = os.getenv('YOUTUBE_API_KEY')

        if not api_key:
            raise ValueError("Chave da API do YouTube não encontrada")
        return build('youtube', 'v3', developerKey=api_key)

    @action(detail=False, methods=['get'])
    def search_videos(self, request):
        """
        Busca vídeos do YouTube baseado no parâmetro 'game' na query string.
        """
        game = request.query_params.get('game')

        if not game:
            return Response(
                {"error": "O parâmetro 'game' é obrigatório"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            youtube = self.get_youtube_service()
            
            # Faz a requisição de busca
            request = youtube.search().list(
                part='snippet',
                q=game,
                type='video',
                order='date',
                maxResults=3
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
            
            # Serializa os resultados
            serializer = YouTubeVideoSerializer(videos, many=True)
            return Response(serializer.data)
            
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )