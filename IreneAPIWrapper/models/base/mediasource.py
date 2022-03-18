from . import File


class MediaSource(File):
    r"""Represents a MediaSource object.

    A MediaSource object inherits from :ref:`File`.

    Attributes
    ----------
    id: int
        The Media id.
    file_type: str
        The file type (if it is known).
    url: str
        The URL of the media.
    """
    def __init__(self, url, file_type=None):
        # TODO: file location
        super(MediaSource, self).__init__(file_type=file_type)
        self.url = url
