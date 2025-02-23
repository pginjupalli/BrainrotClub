from django.db import models
import uuid


class Post(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    title = models.CharField(max_length=100)
    club_name = models.CharField(max_length=100)

    body = models.TextField(null=True, blank=True)
    date_posted = models.DateTimeField(auto_now_add=True)

    video = models.ForeignKey("Video", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.uuid} ({self.title}: {self.club_name})"


class Video(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    file = models.FileField(upload_to="videos/", null=True, blank=True)
    thumbnail = models.FileField(upload_to="thumbnails/", null=True, blank=True)

    def url(self):
        return self.file.url

    def thumbnail_url(self):
        return self.thumbnail.url

    def __str__(self):
        return f"{self.uuid}"


