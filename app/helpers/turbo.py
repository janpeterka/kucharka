def remove(self, target):
    """Create a remove stream.
    :param target: the target ID for this change.
    """
    return self._make_stream("remove", "", target)
