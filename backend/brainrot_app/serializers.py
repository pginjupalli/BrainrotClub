from . import models, serializers

from rest_framework import serializers as rf_serializers


class VideoSerializer(rf_serializers.ModelSerializer):
    class Meta:
        model = models.Video
        fields = ["uuid", "file", "thumbnail"]


class PostSerializer(rf_serializers.ModelSerializer):
    video = serializers.VideoSerializer()

    class Meta:
        model = models.Post
        fields = ["uuid", "club_name", "title", "body", "date_posted", "video"]
