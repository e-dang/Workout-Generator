from django.core.management.base import BaseCommand
from django.core.management import call_command


class Command(BaseCommand):
    help = 'Loads all MuscleSubPortions defined in the fixture muscle_subportions.json into the database.'

    def handle(self, *args, **options):
        call_command('loaddata', 'muscle_subportions.json')
        self.stdout.write(self.style.SUCCESS('Successfully imported MuscleSubPortions!'))
