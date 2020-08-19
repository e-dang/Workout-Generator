from collections import namedtuple

import pytest

from main import utils


@pytest.mark.parametrize('model, kwargs, expected_kwargs, expected_extras', [
    (namedtuple('Test', 'x y c'), {'x': 1, 'a': 1, '2': 1}, {'x': 1}, {'a': 1, '2': 1}),
    (namedtuple('Test', ''), {'x': 1, 'a': 1, '2': 1}, {}, {'x': 1, 'a': 1, '2': 1}),
    (None, {'x': 1, 'a': 1, '2': 1}, {}, {'x': 1, 'a': 1, '2': 1}),
    (namedtuple('Test', 'x y c'), {}, {}, {})
],
    ids=['extra subset of kwargs', 'no attrs on model', 'model is None', 'empty kwargs'])
def test_split_dict_on_model_attrs(model, kwargs, expected_kwargs, expected_extras):
    extras = utils.split_dict_on_model_attrs(model, kwargs)

    assert kwargs == expected_kwargs
    assert extras == expected_extras


@pytest.mark.parametrize('model, kwargs, force', [
    (namedtuple('Test', 'x y c'), {'z': 3}, False),
    (namedtuple('Test', 'x y c'), {'x': 3}, True),
    (namedtuple('Test', 'x y c'), {}, True),
    (namedtuple('Test', 'x y c'), {}, False)
],
    ids=['add new attr', 'replace current attr', 'no new atts force', 'no new atts no force'])
def test_apply_attrs_to_model(model, kwargs, force):
    new_model = utils.apply_attrs_to_model(model, kwargs, force=force)

    for key, value in kwargs.items():
        attr = '_' + str(key)
        assert hasattr(new_model, attr)
        assert getattr(new_model, attr) == value

    for attr in dir(model):
        assert hasattr(new_model, attr)


@pytest.mark.parametrize('model, kwargs, force', [
    (None, {'z': 3}, False),
    (None, {'z': 3}, True),
    (namedtuple('Test', 'x y c'), {'x': 3}, False)
],
    ids=['model is None no force', 'model is None force', 'replace current attr no force'])
def test_apply_attrs_to_model_fail(model, kwargs, force):
    if model is not None:
        model._x = None

    with pytest.raises(ValueError):
        _ = utils.apply_attrs_to_model(model, kwargs, force=force)
