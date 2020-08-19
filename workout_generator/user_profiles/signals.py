import os

from django.db.models.signals import post_save
from django.dispatch import receiver

from user_profiles.models import UserProfile
from users.models import User
from main import utils


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        extra_fields = [field.name for field in UserProfile._meta.get_fields()]
        extra_values = utils.extract_extra_fields_from_model(instance, extra_fields)
        profile = UserProfile.objects.create(user=instance, **extra_values)
        profile.make_follow_request(UserProfile.objects.get(user__email=os.environ.get('GLOBAL_EMAIL')))


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()
