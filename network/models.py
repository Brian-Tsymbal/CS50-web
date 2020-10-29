from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.serializers import serialize


class User(AbstractUser):
    pass


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.CharField(max_length=280, blank=False)
    likes = models.PositiveIntegerField(default=0)
    timestamp = models.DateTimeField(auto_now_add=True)

    def serialize(self):
        return{
            "id": self.id,
            "user": self.user.username,
            "body": self.body,
            "likes": self.likes,
            "timestamp": self.timestamp.strftime("%b %#d %Y, %#I:%M %p"),

        }


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item = models.ForeignKey(Post, on_delete=models.CASCADE)

    def serialize(self):
        return{
            "id": self.id,
            "user": self.user.username,
            "post": self.item.id
        }

    class Meta:
        unique_together = ["user", "item"]


class Follow(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="active_user")
    following = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="follwed_user")

    def serialize(self):
        return{
            "id": self.id,
            "user": self.user.username,
            "followed_user": self.following.username,
            "true": True
        }
