from rest_framework import generics
from . import models, serializers
from rest_framework.response import Response

# Create your views here.


class PostList(generics.ListCreateAPIView):
    queryset = models.Post.objects.all()
    serializer_class = serializers.PostSerializer

    # override the get method to not show Posts without a Video
    def get_queryset(self):
        return self.queryset.exclude(video__isnull=True)

    # override the create method to ignore the video field and create a video manually
    def post(self, request, *args, **kwargs):
        if not request.data.get("details"):
            return Response({"details": "This field is required."}, status=400)

        video = models.Video.objects.create()
        # video.file = "videos/video.txt"
        # video.thumbnail = "thumbnails/thumbnail.txt"
        # video.save()

        request.data.pop("details", None)

        post = models.Post.objects.create(video=video, **request.data)

        return Response(self.get_serializer(post).data)
