from typing import Union, List, Optional, Dict

from IreneAPIWrapper.sections import outer
from . import CallBack, Access, AbstractModel, internal_fetch, internal_fetch_all, MediaSource, Affiliation


class Media(AbstractModel):
    def __init__(self, *args, **kwargs):
        super(Media, self).__init__()
        self.id = kwargs.get("mediaid")
        self.faces: int = kwargs.get("faces")
        self.affiliation: Affiliation = Affiliation(kwargs.get("affiliationid"))
        self.enabled = kwargs.get("enabled")

        self.source: MediaSource = MediaSource(url=kwargs.get("link"), file_type=kwargs.get("filetype"))
        self.banner: MediaSource = MediaSource(url=kwargs.get("banner"), file_type=kwargs.get("filetype"))
        _media[self.id] = self

    async def create(self, *args, **kwargs):
        # TODO : create
        return Media(*args)

    @staticmethod
    async def get(media_id: int):
        """Get a media object.

        If the Media object does not exist in cache, it will fetch the name from the API.
        :param media_id: (int) The ID of the name to get/fetch.
        """
        existing_person = _media.get(media_id)
        if not existing_person:
            return await Media.fetch(media_id)

    @staticmethod
    async def fetch(media_id: int):
        """Fetch an updated Media object from the API.

        # NOTE: Media objects are added to cache on creation.

        :param media_id: (int) The media's ID to fetch.
        """
        return internal_fetch(obj=Media, request={
            'route': 'media/$media_id',
            'media_id': media_id,
            'method': 'GET'}
        )

    @staticmethod
    async def fetch_all():
        """Fetch all media.

        # NOTE: Media objects are added to cache on creation.
        """
        return internal_fetch_all(obj=Media, request={
            'route': 'media/',
            'method': 'GET'}
        )


_media: Dict[int, Media] = dict()
