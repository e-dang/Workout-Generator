import pytest
import mock

from muscles.models import Muscle, MuscleGrouping, MuscleSubPortion


@pytest.mark.parametrize('obj_type', [
    MuscleSubPortion,
    Muscle,
    MuscleGrouping
], ids=['muscle subportion', 'muscle', 'muscle grouping'])
def test_muscle_str(obj_type):
    name = 'lower traps'
    mock_obj = mock.MagicMock()
    mock_obj.name = name

    assert obj_type.__str__(mock_obj) == name.capitalize()
