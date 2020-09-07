import pytest

from muscles.models import Muscle, MuscleGrouping, MuscleSubPortion
from django.db.utils import DataError
from django.core.exceptions import ValidationError


@pytest.mark.parametrize('obj_type', [
    MuscleSubPortion,
    Muscle,
    MuscleGrouping
], ids=['muscle subportion', 'muscle', 'muscle grouping'])
@pytest.mark.django_db
def test_aliases(obj_type):
    name = 'shoulders'
    other_names = ['deltoids', 'delts']
    obj = obj_type.objects.create(name=name, other_names=other_names)

    assert obj.aliases == [name] + other_names


@pytest.mark.parametrize('obj_type', [
    MuscleSubPortion,
    Muscle,
    MuscleGrouping
], ids=['muscle subportion', 'muscle', 'muscle grouping'])
@pytest.mark.parametrize('data, error', [
    ({'name': 'teeeeeeeeeeeeeeeeeeeeeeest', 'other_names': []}, DataError),
    ({'name': 'test', 'other_names': ['teeeeeeeeeeeeeeeeeeeeeeest']}, ValidationError)
],
    ids=['name too long', 'other name too long'])
@pytest.mark.django_db
def test_invalid_name_lengths(obj_type, data, error):

    with pytest.raises(error):
        obj = obj_type.objects.create(**data)
        obj.full_clean()
