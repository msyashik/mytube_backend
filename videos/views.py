from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from authors.models import Author
from .serializers import VideoSerializer, VideoDetailSerializer
from .models import Video

# Create your views here.
class VideoList(APIView):
    """getting all the videos with title and youtube video id"""
    def get(self, request, format=None):
        videos = Video.objects.all()
        serializer = VideoSerializer(videos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    """creating new video in the database"""
    def post(self, request, format=None):
        try:
            video_id = request.data.get("video_id")
            title = request.data.get("title")
            author_email = request.data.get("author_email")
            try:
                author = Author.objects.get(email=author_email)
                is_video_present = Video.objects.filter(video_id=video_id)
                if len(is_video_present) > 0:
                    msg = "Video is already added"
                    return Response(msg, status=status.HTTP_400_BAD_REQUEST)
                else:
                    new_video = Video(video_id=video_id, title=title, author=author)
                    new_video.save()
                return Response("successful", status=status.HTTP_201_CREATED) 
            except Author.DoesNotExist:
                msg = "Author does not exist"
                return Response(msg, status=status.HTTP_400_BAD_REQUEST)
            return Response("okay")
        except BaseException:
            msg = "Please provide sufficient data"
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)


class VideoDetail(APIView):
    def get(self, request, pk, format=None):
        try:
            video = Video.objects.get(video_id=pk)
            data = get_video_details(video.video_id)
            return Response(data, status=status.HTTP_200_OK)
        except Video.DoesNotExist:
            msg = "Video id is not valid"
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)


class VideoViews(APIView):
    def post(self, request, format=None):
        try:
            video_id = request.data.get("video_id")
            try:
                is_video_present = Video.objects.get(video_id=video_id)
                is_video_present.view_count += 1
                is_video_present.save()
                data = get_video_details(video_id)
                return Response(data, status=status.HTTP_200_OK)
            except Video.DoesNotExist:
                msg = "Video doesn't exist"
                return Response(msg, status=status.HTTP_400_BAD_REQUEST) 
        except BaseException:
            msg = "Please provide sufficient data"
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)


class VideoLikes(APIView):
    def post(self, request, format=None):
        try:
            video_id = request.data.get("video_id")
            author_email = request.data.get("author_email")
            try:
                video = Video.objects.get(video_id=video_id)
                author = Author.objects.get(email=author_email)
                if video.users_dislike is None:
                    video.users_dislike = []
                    video.save()
                try:
                    dislike_index = video.users_dislike.index(author_email)
                except:
                    dislike_index = None
                if dislike_index is not None:
                    del video.users_dislike[dislike_index]
                    video.dislike_count -= 1
                    video.save()
                if video.users_like is None:
                    video.users_like = []
                    video.save()
                try:
                    like_index = video.users_like.index(author_email)
                except:
                    like_index = None
                if like_index is None:
                    video.users_like.append(author_email)
                    video.like_count += 1
                    video.save()
                else:
                    del video.users_like[like_index]
                    video.like_count -= 1
                    video.save()
                data = get_video_details(video_id)
                return Response(data, status=status.HTTP_200_OK)
            except Video.DoesNotExist:
                msg = "Video does not exist"
                return Response(msg, status=status.HTTP_400_BAD_REQUEST)
            except Author.DoesNotExist:
                msg = "Author does not exist"
                return Response(msg, status=status.HTTP_400_BAD_REQUEST)
        except BaseException:
            msg = "Please provide sufficient data"
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)


class VideoDislikes(APIView):
    def post(self, request, format=None):
        try:
            video_id = request.data.get("video_id")
            author_email = request.data.get("author_email")
            try:
                video = Video.objects.get(video_id=video_id)
                author = Author.objects.get(email=author_email)
                if video.users_like is None:
                    video.users_like = []
                    video.save()
                try:
                    like_index = video.users_like.index(author_email)
                except:
                    like_index = None
                if like_index is not None:
                    del video.users_like[like_index]
                    video.like_count -= 1
                    video.save()
                if video.users_dislike is None:
                    video.users_dislike = []
                    video.save()
                try:
                    dislike_index = video.users_dislike.index(author_email)
                except:
                    dislike_index = None
                if dislike_index is None:
                    video.users_dislike.append(author_email)
                    video.dislike_count += 1
                    video.save()
                else:
                    del video.users_dislike[dislike_index]
                    video.dislike_count -= 1
                    video.save()
                data = get_video_details(video_id)
                return Response(data, status=status.HTTP_200_OK)
            except Video.DoesNotExist:
                msg = "Video does not exist"
                return Response(msg, status=status.HTTP_400_BAD_REQUEST)
            except Author.DoesNotExist:
                msg = "Author does not exist"
                return Response(msg, status=status.HTTP_400_BAD_REQUEST)
        except BaseException:
            msg = "Please provide sufficient data"
            return Response(msg, status=status.HTTP_400_BAD_REQUEST)


def get_video_details(video_id: str):
    video = Video.objects.get(video_id=video_id)
    if video.users_like is None:
        video.users_like = []
        video.save()
    if video.users_dislike is None:
        video.users_dislike = []
        video.save()
    users_like_email = video.users_like
    users_like_name = []
    for email in users_like_email:
        author = Author.objects.get(email=email)
        users_like_name.append(author.name)
    users_dislike_email = video.users_dislike
    users_dislike_name = []
    for email in users_dislike_email:
        author = Author.objects.get(email=email)
        users_dislike_name.append(author.name)
    data = {
        "video_id": video_id,
        "title": video.title,
        "author": video.author.name,
        "view_count": video.view_count,
        "like_count": video.like_count,
        "dislike_count": video.dislike_count,
        "users_like": users_like_name,
        "users_dislike": users_dislike_name,
        "users_like_email": users_like_email,
        "users_dislike_email": users_dislike_email
    }
    return data