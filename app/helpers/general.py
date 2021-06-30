def empty_object():
    import types

    obj = types.SimpleNamespace()
    return obj


def list_without_duplicated(array):
    return list(dict.fromkeys(array))
