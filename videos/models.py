from django.db import models
from authors.models import Author
from django.contrib.postgres.fields import ArrayField

# # Create your models here.
class Video(models.Model):
    video_id = models.CharField(max_length=200, unique=True)
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    like_count = models.IntegerField(default=0)
    dislike_count = models.IntegerField(default=0)
    view_count = models.IntegerField(default=0)
    users_like = ArrayField(models.CharField(max_length=200), blank=True, null=True)
    users_dislike = ArrayField(models.CharField(max_length=200), blank=True, null=True)

    def __str__(self):
        return self.video_id
    

