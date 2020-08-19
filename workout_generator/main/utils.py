
def split_dict_on_model_attrs(model, kwargs):
    if model is None:
        extras = dict(kwargs)
        kwargs.clear()
        return extras

    if len(kwargs) == 0:
        return {}

    extras = {}
    for key in list(kwargs):
        if not hasattr(model, key):
            extras[key] = kwargs.pop(key)

    return extras


def create_attr_string(base_attr):
    try:
        return '_' + str(base_attr)
    except TypeError:
        raise TypeError(
            f'Invalid type {type(base_attr)} for a base attribute name - The base attribute name must be castable to a string')


def apply_attrs_to_model(model, kwargs, force=False):
    if model is None:
        raise ValueError('Cannot apply attributes to None')
    elif len(kwargs) == 0:
        return model

    for key, value in kwargs.items():
        attr = create_attr_string(key)
        if not hasattr(model, attr) or force:
            setattr(model, attr, value)
        else:
            raise ValueError(f'The model already has the attribute {attr}. To override attributes set force = True.')

    return model
