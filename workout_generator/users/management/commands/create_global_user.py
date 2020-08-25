import os

from django.core.management.base import BaseCommand, CommandError

from users.models import User
from user_profiles.models import UserProfile


class Command(BaseCommand):
    help = '''Creates the global User instance.'''

    def handle(self, *args, **options):
        global_email = os.environ.get('GLOBAL_EMAIL', None)
        global_password = os.environ.get('GLOBAL_PASSWORD', None)

        if global_email is None or global_password is None:
            raise CommandError('The environment variables GLOBAL_EMAIL and GLOBAL_PASSWORD must be set!')

        try:
            _ = User.objects.get(email=global_email)
            raise CommandError('The global User instance has already been made!')
        except User.DoesNotExist:
            pass

        User.objects.create_superuser(email=global_email, password=global_password,
                                      visibility=UserProfile.PUBLIC)
        self.stdout.write(self.style.SUCCESS('Successfully created the global User instance!'))
