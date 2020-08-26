from django.core.management import call_command
from django.core.management.base import BaseCommand, CommandError

from muscles.models import Muscle, MuscleSubPortion


class Command(BaseCommand):
    help = '''Loads all Muscles defined in the fixture muscles.json into the database and create Muscle instances from
    all instances of MuscleSubPortions currently in the database.'''

    def handle(self, *args, **options):
        muscle_subportions = MuscleSubPortion.objects.all()
        if len(muscle_subportions) == 0:
            raise CommandError(f'There are no MuscleSubPortions currently in the database. Please load these first!')

        # load Muscles from fixture
        call_command('loaddata', 'muscles.json')

        # create Muscle from MuscleSubPortion
        for muscle_subportion in muscle_subportions:
            muscle = Muscle.objects.create(name=muscle_subportion.name, other_names=muscle_subportion.other_names)
            muscle.save()
            muscle.subportions.add(muscle_subportion)

        self.stdout.write(self.style.SUCCESS('Successfully imported Muscles!'))
