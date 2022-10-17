from typing import Union, List, Optional, Dict

from IreneAPIWrapper.sections import outer
from . import (
    CallBack,
    Access,
    AbstractModel,
    internal_fetch,
    internal_fetch_all,
    MediaSource,
    Affiliation,
    internal_insert,
    internal_delete,
    basic_call,
)


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

    def __init__(
        self,
        media_id,
        source,
        faces,
        affiliation,
        is_enabled,
        is_nsfw,
        failed=0,
        correct=0,
    ):
        super(Media, self).__init__(media_id)
        self.source: MediaSource = source
        self.faces: int = faces
        self.affiliation: Affiliation = affiliation
        self.is_enabled: bool = is_enabled
        self.is_nsfw: bool = is_nsfw
        self.failed_guesses = failed
        self.correct_guesses = correct

        if not _media.get(self.id):
            _media[self.id] = self

    @property
    def difficulty(self):
        """Get the difficulty (ratio) of the media."""
        if self.failed_guesses + self.correct_guesses < 100:
            return None

        return self.correct_guesses / (self.correct_guesses + self.failed_guesses)

    @property
    def url(self):
        """Get the media source url."""
        if self.source:
            return self.source.url

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

        source = MediaSource(url=link, media_id=media_id, file_type=file_type)

        affiliation_id = kwargs.get("affiliationid")
        affiliation: Affiliation = await Affiliation.get(affiliation_id)

        failed = kwargs.get("failed") or 0
        correct = kwargs.get("correct") or 0

        is_enabled = kwargs.get("enabled")
        is_nsfw = kwargs.get("nsfw")

        Media(
            media_id, source, faces, affiliation, is_enabled, is_nsfw, failed, correct
        )
        return _media[media_id]

    async def fetch_image_host_url(self):
        if self.source:
            image_host_url = (
                self.source.image_host_url
                or await self.source.download_and_get_image_host_url()
            )
            return image_host_url or self.source.url

    async def upsert_guesses(self, correct: bool):
        """
        Increment the guesses appropriately and update to the database after the total amount is divisible by 5.

        :param correct: bool
            Whether the user guessed correctly.
        """
        if correct:
            self.correct_guesses += 1
        else:
            self.failed_guesses += 1

        if (self.correct_guesses + self.failed_guesses) % 5 == 0:
            await basic_call(
                request={
                    "route": "media/$media_id",
                    "media_id": self.id,
                    "failed_guesses": self.failed_guesses,
                    "correct_guesses": self.correct_guesses,
                    "method": "POST",
                }
            )

    async def delete(self) -> None:
        """
        Delete the Media object from the database and remove it from cache.

        :returns: None
        """
        await internal_delete(
            self,
            request={
                "route": "media/$media_id",
                "media_id": self.id,
                "method": "DELETE",
            },
        )
        await self._remove_from_cache()

    async def _remove_from_cache(self) -> None:
        """
        Remove the Media object from cache.

        :returns: None
        """
        _media.pop(self.id)

    @staticmethod
    async def insert(
        link, face_count, file_type, affiliation_id, enabled, is_nsfw
    ) -> None:
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
        await internal_insert(
            request={
                "route": "media",
                "link": link,
                "faces": face_count,
                "file_type": file_type,
                "affiliation_id": affiliation_id,
                "enabled": enabled,
                "is_nsfw": is_nsfw,
                "method": "POST",
            }
        )

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
    async def get_random(
        object_id: int,
        affiliation=False,
        person=False,
        group=False,
        min_faces=1,
        max_faces=999,
        can_be_nsfw=False,
        is_enabled=True,
        file_type=None,
    ):
        """Get a random Media object from the API.

        :param object_id: int
            The object ID to grab media for.
            This can be an affiliation, person, group, or media (default) ID if specified.
        :param affiliation: bool
            If the object ID is an Affiliation ID.
        :param person: bool
            If the object ID is a Person ID.
        :param group: bool
            If the object ID is a Group ID.
        :param min_faces: int
            Minimum number of faces the media can have
        :param max_faces: int
            Maximum number of faces the media can have
        :param can_be_nsfw: bool
            If it is okay to have NSFW media.
        :param is_enabled: bool
            The media object is officially active.
        :param file_type: str
            A restricted file type.
        """
        request = {
            "method": "POST",
            "min_faces": min_faces,
            "max_faces": max_faces,
            "file_type": file_type,
            "nsfw": can_be_nsfw,
            "enabled": is_enabled,
        }
        if affiliation:
            request["route"] = "affiliation/$affiliation_id/media"
            request["affiliation_id"] = object_id
        elif person:
            request["route"] = "person/$person_id/media"
            request["person_id"] = object_id
        elif group:
            request["route"] = "group/$group_id/media"
            request["group_id"] = object_id
        # one does not exist for media id since it cannot be filtered.
        # Although it is possible to pass it into the API.
        callback = await basic_call(request=request)
        results = callback.response.get("results")
        if results:
            media = await Media.get(results["mediaid"])
            if media.source:
                media.source.image_host_url = results["host"]
            return media

    @staticmethod
    async def get_all(affiliations: List[Affiliation] = None, limit=None, count_only=False):
        """
        Get all Media objects in cache or from the API.

        :param affiliations: Optional[List[:ref:`Affiliation`]]
            A list of affiliations that must belong with the media.
        :param limit: Optional[int]
            A maximum number of results to be sent if fetched.
        :param count_only: bool
            Whether to only return the number of available media.

        :returns: dict_values[:ref:`Media`]
            All Media objects from cache/API.
        :returns: int
            The number of media objects available for the affiliations if count_only is set to True.
        """
        if affiliations is None:
            return _media.values()

        callback = await basic_call(
            request={
                "route": "media/affiliations",
                "affiliation_ids": [aff.id for aff in affiliations],
                "limit": limit,
                "count_only": count_only,
                "method": "GET",
            }
        )
        results = callback.response.get("results")
        if not results:
            return []

        if count_only:
            return sum([media_info["mediaid"] for media_info in results.values()])

        media_objs = [
            await Media.get(media_info["mediaid"])
            for media_info in results.values()
        ]
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
                "route": "affiliation/$affiliation_id/media",
                "affiliation_id": object_id,
            }
        elif person:
            request = {
                "route": "person/$person_id/media",
                "person_id": object_id,
            }
        elif group:
            request = {
                "route": "group/$group_id/media",
                "group_id": object_id,
            }
        else:  # Default - Media ID
            request = {
                "route": "media/$media_id",
                "media_id": object_id,
            }
        request["method"] = "GET"

        return await internal_fetch(obj=Media, request=request)

    @staticmethod
    async def fetch_all():
        """Fetch all media.

        .. NOTE::: Media objects are added to cache on creation.
        """
        return await internal_fetch_all(
            obj=Media, request={"route": "media/", "method": "GET"}
        )


_media: Dict[int, Media] = dict()
