from typing import Union, List, Optional, Dict

from IreneAPIWrapper.sections import outer
from . import (
    CallBack,
    Access,
    AbstractModel,
    internal_fetch,
    internal_fetch_all,
    internal_insert,
    internal_delete,
)


class Tag(AbstractModel):
    r"""Represents a tag that describes an entity.

    A Tag object inherits from :ref:`AbstractModel`.

    Parameters
    ----------
    tag_id: int
        The Tag's id.
    name: str
        The tag's name.

    Attributes
    ----------
    id: int
        The Tag id.
    name: str
        The tag name.
    """

    def __init__(self, tag_id, name, *args, **kwargs):
        super(Tag, self).__init__(tag_id)
        self.name = name

        if not _tags.get(self.id):
            _tags[self.id] = self

    def __str__(self):
        return self.name

    @staticmethod
    async def create(*args, **kwargs):
        """
        Create a Tag object.

        :returns: :ref:`Tag`
        """
        tag_id = kwargs.get("tagid")
        name = kwargs.get("name")
        Tag(tag_id, name)
        return _tags[tag_id]

    async def delete(self) -> None:
        """
        Delete the Tag object from the database and remove it from cache.

        :returns: None
        """
        await internal_delete(
            self,
            request={"route": "tag/$tag_id", "tag_id": self.id, "method": "DELETE"},
        )
        await self._remove_from_cache()

    @staticmethod
    async def insert(tag_name) -> None:
        """
        Insert a new Tag into the database.

        :param tag_name:
        :returns: None
        """
        await internal_insert(
            request={"route": "tag", "name": tag_name, "method": "POST"}
        )

    async def _remove_from_cache(self) -> None:
        """
        Remove the Tag object from cache.

        :returns: None
        """
        _tags.pop(self.id)

    @staticmethod
    async def get(tag_id: int, fetch=True):
        """
        Get a Tag object.

        If the Tag object does not exist in cache, it will fetch the tag from the API.
        :param tag_id: int
            The ID of the tag to get/fetch.
        :param fetch: bool
            Whether to fetch from the API if not found in cache.
        """
        existing = _tags.get(tag_id)
        if not existing and fetch:
            return await Tag.fetch(tag_id)
        return existing

    @staticmethod
    async def get_all():
        """
        Get all Tag objects in cache.

        :returns: dict_values[:ref:`Tag`]
            All Tag objects from cache.
        """
        return _tags.values()

    @staticmethod
    async def fetch(tag_id: int):
        """Fetch an updated Tag object from the API.

        .. NOTE::: Tag objects are added to cache on creation.

        :param tag_id: int
            The tag's ID to fetch.
        """
        return await internal_fetch(
            obj=Tag, request={"route": "tag/$tag_id", "tag_id": tag_id, "method": "GET"}
        )

    @staticmethod
    async def fetch_all():
        """Fetch all tags.

        .. NOTE::: Tag objects are added to cache on creation.
        """
        return await internal_fetch_all(
            obj=Tag, request={"route": "tag/", "method": "GET"}
        )


_tags: Dict[int, Tag] = dict()
