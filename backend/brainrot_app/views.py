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
        if not request.data.get("details"):
            return Response({"details": "This field is required."}, status=400)
        if not request.data.get("club_name"):
            return Response({"club_name": "This field is required"}, status=400)
        if not request.data.get("title"):
            return Response({"event_name": "This field is required"}, status=400)
        if not request.data.get("tone"):
            return Response({"tone": "This field is required"}, status=400)
        if not request.data.get("persona"):
            return Response({"persona": "This field is required"}, status=400)
        if not request.data.get("voice"):
            return Response({"voice": "This field is required"}, status=400)

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
        club_name = request.data.get("club_name")
        event_name = request.data.get("title")
        tone = request.data.pop("tone")
        persona = request.data.pop("persona")
        voice = request.data.pop("voice")

        post = models.Post.objects.create(video=video, **request.data)

        response_data = self.get_serializer(post).data

        thread = threading.Thread(
            target=process_video,
            args=(
                details,
                club_name,
                event_name,
                tone,
                persona,
                voice,
                post.uuid,
                video.uuid,
            ),
        )
        thread.start()

        return Response(response_data)


from scripts import heygen
from scripts import movie
# from scripts import perplexity


def process_video(details, club_name, event_name, tone, persona, voice, p_uuid, v_uuid):
    # script = perplexity.perplexity_search(
    #     {
    #         "details": details,
    #         "club_name": club_name,
    #         "event_name": event_name,
    #         "tone": tone,
    #     }
    # )
    script = ""

    video = models.Video.objects.get(pk=v_uuid)
    post = models.Post.objects.get(pk=p_uuid)
    post.body = script
    post.save()

    heygen.get_video(v_uuid, script, avatar_id=persona, voice_id=voice)

    movie.greenscreen_overlay(f"media/videos/{v_uuid}.mp4", "videoB.mp4")

    video.file = f"media/videos/{v_uuid}.mp4"
    video.thumbnail = f"media/thumbnails/{v_uuid}.png"
    video.save()
