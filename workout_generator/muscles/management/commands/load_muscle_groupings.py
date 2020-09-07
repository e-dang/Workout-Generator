from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError

from muscles.models import Muscle, MuscleGrouping


class Command(BaseCommand):
    help = '''Loads all MuscleGroupings defined in the fixture muscle_groupings.json into the database and creates
    MuscleGrouping instances from all instances of Muscle currently in the database.'''

    def handle(self, *args, **options):
        muscles = Muscle.objects.all()
        if len(muscles) == 0:
            raise CommandError(f'There are no Muscles currently in the database. Please load these first!')

        # create MuscleGroupings from fixture
        call_command('loaddata', 'muscle_groupings.json')

        # create MuscleGrouping from Muscle
        for muscle in muscles:
            muscle_grouping = MuscleGrouping.objects.create(name=muscle.name, other_names=muscle.other_names)
            muscle_grouping.save()
            muscle_grouping.muscles.add(muscle)

        self.stdout.write(self.style.SUCCESS('Successfully imported MuscleGroupings!'))
