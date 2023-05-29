from django.urls import path 
from .views import VideoList, VideoViews, VideoDetail, VideoLikes, VideoDislikes

urlpatterns = [
    path("videos/", VideoList.as_view()),
    path("videos/<str:pk>", VideoDetail.as_view()),
    path("video-view/", VideoViews.as_view()),
    path("video-like/", VideoLikes.as_view()),
    path("video-dislike/", VideoDislikes.as_view())
    
]
