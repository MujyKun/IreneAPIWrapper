from typing import Union, List, Optional, Dict

from IreneAPIWrapper.sections import outer
from . import CallBack, Access, AbstractModel, internal_fetch, internal_fetch_all, MediaSource, Affiliation


class Media(AbstractModel):
    def __init__(self, media_id, source, faces, affiliation, is_enabled, is_nsfw):
        super(Media, self).__init__()
        self.id = media_id
        self.source: MediaSource = source
        self.faces: int = faces
        self.affiliation: Affiliation = affiliation
        self.is_enabled: bool = is_enabled
        self.is_nsfw: bool = is_nsfw

        _media[self.id] = self

    @staticmethod
    async def create(*args, **kwargs):
        media_id = kwargs.get("mediaid")

        link = kwargs.get("link")
        faces = kwargs.get("faces")
        file_type = kwargs.get("filetype")

        source = MediaSource(url=link, file_type=file_type)

        affiliation_id = kwargs.get("affiliationid")
        affiliation: Affiliation = await Affiliation.get(affiliation_id)

        is_enabled = kwargs.get("enabled")
        is_nsfw = kwargs.get("nsfw")

        media_args = {media_id, source, faces, affiliation, is_enabled, is_nsfw}

        return Media(*media_args)

    @staticmethod
    async def get(media_id: int, fetch=True):
        """Get a media object.

        If the Media object does not exist in cache, it will fetch the name from the API.
        :param media_id: (int) The ID of the name to get/fetch.
        :param fetch: (bool) Whether to fetch from the API if not found in cache.
        """
        existing = _media.get(media_id)
        if not existing and fetch:
            return await Media.fetch(media_id)
        return existing

    @staticmethod
    async def fetch(media_id: int):
        """Fetch an updated Media object from the API.

        # NOTE: Media objects are added to cache on creation.

        :param media_id: (int) The media's ID to fetch.
        """
        return await internal_fetch(obj=Media, request={
            'route': 'media/$media_id',
            'media_id': media_id,
            'method': 'GET'}
        )

    @staticmethod
    async def fetch_all():
        """Fetch all media.

        # NOTE: Media objects are added to cache on creation.
        """
        return await internal_fetch_all(obj=Media, request={
            'route': 'media/',
            'method': 'GET'}
        )


_media: Dict[int, Media] = dict()
