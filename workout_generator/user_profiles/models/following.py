from django.db import models
from user_profiles.models.user_profile import UserProfile


class Following(models.Model):
    following_user = models.ForeignKey(UserProfile, related_name='following_user', on_delete=models.CASCADE)
    followed_user = models.ForeignKey(UserProfile, related_name='followed_user', on_delete=models.CASCADE)
    created = models.DateField(auto_now_add=True, db_index=True)

    class Meta:
        unique_together = ('following_user', 'followed_user')
        ordering = ('-created', )

    def __str__(self):
        return f'{str(self.following_user.user)} follows {str(self.followed_user.user)}'
