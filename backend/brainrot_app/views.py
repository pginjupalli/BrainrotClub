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
        return self.queryset.exclude(video__isnull=True).order_by("-date_posted")

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
        if not request.data.get("bg"):
            return Response({"bg": "This field is required"}, status=400)

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
        bg = request.data.pop("bg")

        load = False
        if request.data.get("load"):
            request.data.pop("load")
            load = True

        print(load)

        post = models.Post.objects.create(video=video, **request.data)

        if load:
            video.file = f"videos/hackathon.mp4"
            video.thumbnail = f"thumbnails/hackathon.png"
            video.save()
            post.body = """Hey there, tech enthusiasts and changemakers! Are you ready for the most exciting event of the year? It's HopperHacks, brought to you by WiCS!
Imagine a day filled with coding, creativity, and making a real difference in the world. That's exactly what HopperHacks is all about! We're talking about a social good-focused hackathon that'll blow your mind!
Got ideas to tackle mental health issues? Want to revolutionize education? Or maybe you're passionate about saving our planet? Whatever your cause, HopperHacks is your chance to shine!
Join us for an unforgettable day where you'll apply your tech skills to solve real-world problems. We're talking about issues that affect societies globally – and you'll be at the forefront of creating solutions!
Whether you're a coding wizard or just starting out, HopperHacks welcomes all! Team up with like-minded individuals, brainstorm innovative ideas, and turn them into reality. Who knows? Your project might just change the world!
So, what are you waiting for? Mark your calendars, grab your laptops, and get ready to hack for good! HopperHacks is coming, and trust me, you don't want to miss this! See you there, future world-changers!"""
            post.save()
            response_data = self.get_serializer(post).data
            return Response(response_data)
        else:
            thread = threading.Thread(
                target=process_video,
                args=(
                    bg,
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

        response_data = self.get_serializer(post).data
        return Response(response_data)


from scripts import heygen
from scripts import movie
from scripts import perplexity


def process_video(
    bg, details, club_name, event_name, tone, persona, voice, p_uuid, v_uuid
):
    script = perplexity.perplexity_search(
        {
            "details": details,
            "club_name": club_name,
            "event_name": event_name,
            "tone": tone,
        }
    )

    video = models.Video.objects.get(pk=v_uuid)
    post = models.Post.objects.get(pk=p_uuid)
    post.body = script
    post.save()

    print(script)

    heygen.get_video(v_uuid, script[:200], avatar_id=persona, voice_id=voice)

    movie.greenscreen_overlay(
        f"media/videos/{v_uuid}_green.mp4", bg, f"media/videos/{v_uuid}.mp4"
    )

    video.file = f"videos/{v_uuid}.mp4"
    video.thumbnail = f"thumbnails/{v_uuid}.png"
    video.save()
