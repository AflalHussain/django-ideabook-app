from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UserProfile(models.Model):
    profile_user   = models.OneToOneField(User,related_name='profile_user', on_delete=models.CASCADE)
    profile_pic = models.ImageField(blank=True,null=True,)

class UserFollowing(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE,related_name="following")
    following_user=models.ForeignKey(User, related_name="followers",on_delete=models.CASCADE)
    followed_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user','following_user'],  name="unique_followers")
        ]

        ordering = ["-followed_date"]

    def __str__(self):
        return f"{self.user.username} follows {self.following_user.username}"