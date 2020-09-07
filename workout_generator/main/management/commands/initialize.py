from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = '''Initialize the database with the global user, muscles and equipment data.'''

    def handle(self, *args, **options):
        call_command('makemigrations')
        call_command('migrate')
        call_command('init_muscles')
        call_command('create_global_user')
        call_command('loaddata', 'equipment.json')

        self.stdout.write(self.style.SUCCESS('Successfully initialized the database!'))
