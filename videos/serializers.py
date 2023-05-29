from .models import Video
from rest_framework import serializers

class VideoSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.email", read_only=True)
    class Meta:
        model = Video
        fields = ["video_id", "title", "author"]


class VideoDetailSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source="author.name", read_only=True)
    class Meta:
        model = Video
        fields = ["video_id", "title", "author", "view_count", "like_count", "dislike_count", "users_like", "users_dislike"]



