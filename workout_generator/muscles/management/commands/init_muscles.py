from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = '''Loads all MuscleSubportions, Muscles, and MuscleGroupings defined in the fixtures muscle_subportions.json,
    muscles.json, muscle_groupings.json by calling the commands load_muscle_subportions, load_muscles, and
    load_muscle_groupings.'''

    def handle(self, *args, **options):
        call_command('load_muscle_subportions')
        call_command('load_muscles')
        call_command('load_muscle_groupings')
