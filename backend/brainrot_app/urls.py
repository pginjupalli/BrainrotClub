from . import views
from django.urls import path

urlpatterns = [
    path("post/", views.PostList.as_view()),
]
