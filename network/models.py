from django.contrib.auth.models import AbstractUser
from django.db import models

LONG = 256


class User(AbstractUser):

    def __str__(self):
        return f"{self.username}"

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    entry = models.CharField(max_length=LONG, default="No description")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user}: {self.entry} on {self.timestamp}"

    def serialize(self):
        return {
            "id": self.id,
            "user": self.user.username,
            "entry": self.entry,
            "timestamp": self.timestamp.strftime("%b %-d %Y, %-I:%M %p")
        }


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} liked {self.post}"


class Follow(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="follower")
    following = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user} is following {self.following}"
