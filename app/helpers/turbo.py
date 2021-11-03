def after(self, target):
    """Create a after stream.
    :param target: the target ID for this change.
    """
    return self._make_stream("after", "", target)


def before(self, target):
    """Create a before stream.
    :param target: the target ID for this change.
    """
    return self._make_stream("before", "", target)
