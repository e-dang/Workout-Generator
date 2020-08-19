
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
