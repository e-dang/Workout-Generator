import os

from django.db.models.signals import post_save
from django.dispatch import receiver

from user_profiles.models import UserProfile
from users.models import User


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = UserProfile.objects.create(user=instance)
        profile.follow_user(UserProfile.objects.get(user__email=os.environ.get('GLOBAL_EMAIL')))


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
