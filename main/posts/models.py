from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    title = models.CharField(max_length=250)
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class Likes(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.post.title