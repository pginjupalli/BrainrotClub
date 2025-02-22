# views.py
import threading
from rest_framework import generics
from . import models, serializers
from rest_framework.response import Response

# Create your views here.
class PostList(generics.ListCreateAPIView):
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer

    # Only show posts that have a Video
    def get_queryset(self):
        return self.queryset.exclude(video__isnull=True)

    def post(self, request, *args, **kwargs):
        if not request.data.get("details"): return Response({"details": "This field is required."}, status=400)
        if not request.data.get("name"): return Response({"name": "This field is required"}, status=400)
        if not request.data.get("audience"): return Response({"audience": "This field is required"}, status=400)
        if not request.data.get("tone"): return Response({"tone": "This field is required"}, status=400)
        if not request.data.get("colors"): return Response({"colors": "This field is required"}, status=400)
        if not request.data.get("persona"): return Response({"persona": "This field is required"}, status=400)
        if not request.data.get("voice"): return Response({"voice": "This field is required"}, status=400)

        # Create the video without setting file or thumbnail yet.
        video = models.Video.objects.create()

        # event_config = {
        #     "name": "SBU Hackathon 2024",
        #     "audience": "CS students, developers",
        #     "details": "Date: Oct 2024, Prizes: $10k",
        #     "tone": "energetic",
        #     "colors": "Red, Black",
        #     "persona": "Andrew",
        #     "voice": "Andrew"
        # }
        
        details = request.data.pop("details")
        name = request.data.pop("name")
        audience = request.data.pop("audience")
        tone = request.data.pop("tone")
        colors = request.data.pop("colors")
        persona = request.data.pop("persona")
        voice = request.data.pop("voice")
        
        post = models.Post.objects.create(video=video, **request.data)

        # Serialize the post data for the response.
        response_data = self.get_serializer(post).data
        
        thread = threading.Thread(
            target=process_video,
            args=(details, name, audience, tone, colors, persona, voice, video.uuid)
        )
        thread.start()

        return Response(response_data)

from scripts import heygen
from scripts import movie

def process_video(details, name, audience, tone, colors, persona, voice, v_uuid):
    video = models.Video.objects.get(pk=v_uuid)
    video.file = f"videos/{v_uuid}.mp4"
    video.thumbnail = f"thumbnails/{v_uuid}.png"
    video.save()
