def after(turbo, content, target):
    """Create an append stream.
    :param content: the HTML content to include in the stream.
    :param target: the target ID for this change.
    """
    return turbo._make_stream("after", content, target)
