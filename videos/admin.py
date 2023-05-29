from django.contrib import admin
from .models import Video 

# Register your models here.
class VideoAdmin(admin.ModelAdmin):
    fields = ["video_id", "title", "author", "view_count", "like_count", "dislike_count", "users_like", "users_dislike"]
    list_display = ["video_id", "title", "author","view_count",  "like_count", "dislike_count", "users_like", "users_dislike"]


admin.site.register(Video, VideoAdmin)