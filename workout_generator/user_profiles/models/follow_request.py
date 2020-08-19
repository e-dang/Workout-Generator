from django.db import models
from user_profiles.models import UserProfile


class FollowRequest(models.Model):
    requesting_profile = models.ForeignKey(UserProfile, related_name='requesting_profile', on_delete=models.CASCADE)
    target_profile = models.ForeignKey(UserProfile, related_name='target_profile', on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True, db_index=True)

    class Meta:
        unique_together = ('requesting_profile', 'target_profile')
        ordering = ('-created', )

    def __str__(self):
        return f'User {str(self.requesting_profile.user)} is requesting to follow {str(self.target_profile.user)}'
