import pytest
from collections import namedtuple
from main import utils


@pytest.mark.parametrize('model, kwargs, expected_kwargs, expected_extras', [
    (namedtuple('Test', 'x y c'), {'x': 1, 'a': 1, '2': 1}, {'x': 1}, {'a': 1, '2': 1}),
    (namedtuple('Test', ''), {'x': 1, 'a': 1, '2': 1}, {}, {'x': 1, 'a': 1, '2': 1}),
    (None, {'x': 1, 'a': 1, '2': 1}, {}, {'x': 1, 'a': 1, '2': 1}),
    (namedtuple('Test', 'x y c'), {}, {}, {})
])
def test_split_dict_on_model_attrs(model, kwargs, expected_kwargs, expected_extras):
    extras = utils.split_dict_on_model_attrs(model, kwargs)

    assert kwargs == expected_kwargs
    assert extras == expected_extras
