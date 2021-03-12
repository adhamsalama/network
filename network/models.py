from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime


class User(AbstractUser):
    
    def __str__(self):
        return f"{self.username}" 

class Post(models.Model):
    text = models.TextField()
    date = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(User, related_name="posts", on_delete=models.CASCADE)
    likes = models.ManyToManyField(User, blank=True, related_name="likes")

    def __str__(self):
        return f"{self.text} - {self.user} - {self.date}"

class UserFollowing(models.Model):
    class Meta:
        unique_together = ["user", "followed_user"]
    user = models.ForeignKey(User, related_name="following" ,on_delete=models.CASCADE)
    followed_user = models.ForeignKey(User, null=True, blank=True, related_name="followers", on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.user} following {self.followed_user}"

