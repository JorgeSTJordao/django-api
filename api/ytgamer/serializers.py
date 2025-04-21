from rest_framework import serializers
from datetime import datetime

class YouTubeVideoSerializer(serializers.Serializer):
    title = serializers.CharField()
    video_id = serializers.CharField()
    published_at = serializers.DateTimeField()
    channel_title = serializers.CharField()
    description = serializers.CharField()
    thumbnail_url = serializers.URLField()
    video_url = serializers.SerializerMethodField()

    def get_video_url(self, obj):
        return f"https://www.youtube.com/watch?v={obj['video_id']}"

    class Meta:
        fields = [
            'title',
            'video_id',
            'published_at',
            'channel_title',
            'description',
            'thumbnail_url',
            'video_url'
        ]
        read_only_fields = fields 