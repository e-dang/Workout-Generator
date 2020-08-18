from django.db import models
from user_profiles.models.user_profile import UserProfile


class Followers(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    followers = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True)
