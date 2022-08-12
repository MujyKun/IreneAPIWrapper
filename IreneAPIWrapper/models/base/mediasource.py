from typing import Optional

from . import File, basic_call


class MediaSource(File):
    r"""Represents a MediaSource object.

    A MediaSource object inherits from :ref:`File`.

    Attributes
    ----------
    media_id: int
        The Media id.
    file_type: str
        The file type (if it is known).
    url: str
        The URL of the media.
    """

    def __init__(self, url, media_id: int, file_type=None):
        # TODO: file location
        super(MediaSource, self).__init__(file_type=file_type)
        self.media_id = media_id
        self.url = url
        self.image_host_url: Optional[str] = None

    async def download_and_get_image_host_url(self) -> Optional[str]:
        callback = await basic_call(request={
            'route': "media/download/$media_id",
            'media_id': self.media_id,
            'method': 'GET'
        })
        self.image_host_url = callback.response.get("results")
        return self.image_host_url
