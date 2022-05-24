from typing import Union, List, Optional, Dict

from IreneAPIWrapper.sections import outer
from . import CallBack, Access, AbstractModel, internal_fetch, internal_fetch_all, MediaSource, Affiliation, \
    internal_insert, internal_delete


class Media(AbstractModel):
    r"""Represents a Media object.

    A Media object inherits from :ref:`AbstractModel`.

    Parameters
    ----------
    media_id: int
        The Media ID.
    source: :ref:`MediaSource`
        The :ref:`MediaSource` object that contains information about the media source.
    faces: int
        The amount of faces detected in the image.
    affiliation: :ref:`Affiliation`
        The :ref:`Affiliation` associated with the media.
    is_enabled: bool
        If the media is enabled for usage.
    is_nsfw: bool
        If the media may contain explicit content.

    Attributes
    ----------
    id: int
        The Media ID.
    source: :ref:`MediaSource`
        The :ref:`MediaSource` object that contains information about the media source.
    faces: int
        The amount of faces detected in the image.
    affiliation: :ref:`Affiliation`
        The :ref:`Affiliation` associated with the media.
    is_enabled: bool
        If the media is enabled for usage.
    is_nsfw: bool
        If the media may contain explicit content.
    """
    def __init__(self, media_id, source, faces, affiliation, is_enabled, is_nsfw):
        super(Media, self).__init__(media_id)
        self.source: MediaSource = source
        self.faces: int = faces
        self.affiliation: Affiliation = affiliation
        self.is_enabled: bool = is_enabled
        self.is_nsfw: bool = is_nsfw

        _media[self.id] = self

    @staticmethod
    async def create(*args, **kwargs):
        """
        Create a Media object.

        :returns: :ref:`Media`
        """
        media_id = kwargs.get("mediaid")

        link = kwargs.get("link")
        faces = kwargs.get("faces")
        file_type = kwargs.get("filetype")

        source = MediaSource(url=link, file_type=file_type)

        affiliation_id = kwargs.get("affiliationid")
        affiliation: Affiliation = await Affiliation.get(affiliation_id)

        is_enabled = kwargs.get("enabled")
        is_nsfw = kwargs.get("nsfw")

        return Media(media_id, source, faces, affiliation, is_enabled, is_nsfw)

    async def delete(self) -> None:
        """
        Delete the Media object from the database and remove it from cache.

        :returns: None
        """
        await internal_delete(self, request={
            'route': 'media/$media_id',
            'media_id': self.id,
            'method': 'DELETE'
        })
        await self._remove_from_cache()

    async def _remove_from_cache(self) -> None:
        """
        Remove the Media object from cache.

        :returns: None
        """
        _media.pop(self.id)

    @staticmethod
    async def insert(link, face_count, file_type, affiliation_id, enabled, is_nsfw) -> None:
        """
        Insert a new media into the database.

        :param link: str
            The link of the media.
        :param face_count: int
            Number of faces in the media.
        :param file_type: str
            The file type of the media.
        :param affiliation_id: int
            The affiliation ID associated with the media.
        :param enabled: bool
            Whether the media will be active for searches.
        :param is_nsfw:
            Whether the media may be NSFW.
        :returns: None
        """
        await internal_insert(request={
            'route': 'media',
            'link': link,
            'faces': face_count,
            'file_type': file_type,
            'affiliation_id': affiliation_id,
            'enabled': enabled,
            'is_nsfw': is_nsfw,
            'method': 'POST'
        })

    @staticmethod
    async def get(media_id: int, fetch=True):
        """Get a media object.

        If the Media object does not exist in cache, it will fetch the name from the API.
        :param media_id: int
            The ID of the media to get/fetch.
        :param fetch: bool
            Whether to fetch from the API if not found in cache.
        """
        existing = _media.get(media_id)
        if not existing and fetch:
            return await Media.fetch(media_id)
        return existing

    @staticmethod
    async def get_all(affiliations: List[Affiliation] = None):
        """
        Get all Media objects in cache.

        :returns: dict_values[:ref:`Media`]
            All Media objects from cache.
        """
        if affiliations is None:
            return _media.values()
        else:
            media_objs = []
            for media in _media.values():
                for affiliation in affiliations:
                    if affiliation == media.affiliation:
                        media_objs.append(media)

            return media_objs
    @staticmethod
    async def fetch(object_id: int, affiliation=False, person=False, group=False):
        """Fetch an updated Media object from the API.

        .. NOTE::: Media objects are added to cache on creation.

        :param object_id: int
            The object ID to fetch. This can be an affiliation, person, group, or media (default) ID if specified.
        :param affiliation: bool
            If the object ID is an Affiliation ID.
        :param person: bool
            If the object ID is a Person ID.
        :param group: bool
            If the object ID is a Group ID.
        """
        if affiliation:
            request = {
                'route': 'affiliation/$affiliation_id/media',
                'affiliation_id': object_id,
                'method': 'GET'}
        elif person:
            request = {
                'route': 'person/$person_id/media',
                'person_id': object_id,
                'method': 'GET'}
        elif group:
            request = {
                'route': 'group/$group_id/media',
                'group_id': object_id,
                'method': 'GET'}
        else:  # Default - Media ID
            request = {
                'route': 'media/$media_id',
                'media_id': object_id,
                'method': 'GET'}

        return await internal_fetch(obj=Media, request=request)

    @staticmethod
    async def fetch_all():
        """Fetch all media.

        .. NOTE::: Media objects are added to cache on creation.
        """
        return await internal_fetch_all(obj=Media, request={
            'route': 'media/',
            'method': 'GET'}
        )


_media: Dict[int, Media] = dict()
