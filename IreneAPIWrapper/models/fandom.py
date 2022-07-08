from typing import Union, List, Optional, Dict

from IreneAPIWrapper.sections import outer
from . import (
    CallBack,
    Access,
    AbstractModel,
    internal_fetch,
    internal_fetch_all,
    MediaSource,
    internal_insert,
    internal_delete,
)


class Fandom(AbstractModel):
    r"""Represents the fandom name of a :ref:`Group`.

    A Fandom object inherits from :ref:`AbstractModel`.

    Parameters
    ----------
    group_id: int
        The :ref:`Group` ID.
    fandom_name: str
        The name of the fandom.

    Attributes
    ----------
    id: int
        The :ref:`Group` ID associated with the fandom name.
    name: str
        The name of the fandom.
    """

    def __init__(self, group_id: int, fandom_name: str, *args, **kwargs):
        super(Fandom, self).__init__(group_id)
        self.name = fandom_name
        if not _fandoms.get(self.id):
            _fandoms[self.id] = self

    @staticmethod
    async def create(*args, **kwargs):
        """
        Create a Fandom object.

        :return: :ref:`Fandom`
        """
        group_id = kwargs.get("groupid")
        fandom_name = kwargs.get("name")

        Fandom(int(group_id), fandom_name)
        return _fandoms[int(group_id)]

    async def delete(self) -> None:
        """
        Delete the Fandom object from the database and remove it from cache.

        :returns: None
        """
        await internal_delete(
            self,
            request={
                "route": "fandom/$group_id",
                "group_id": self.id,
                "fandom_name": self.name,
                "method": "DELETE",
            },
        )
        await self._remove_from_cache()

    async def _remove_from_cache(self) -> None:
        """
        Remove the Fandom object from cache.

        :return: None
        """
        _fandoms.pop(self.id)

    @staticmethod
    async def insert(group_id, fandom_name) -> None:
        """
        Insert a new fandom name into the database.

        :param group_id: int
            The :ref:`Group` ID associated with the fandom name
        :param fandom_name: str
            The fandom name of the :ref:`Group`
        :returns: None
        """
        await internal_insert(
            request={
                "route": "fandom/$group_id",
                "group_id": group_id,
                "fandom_name": fandom_name,
                "method": "POST",
            }
        )

    @staticmethod
    async def get(group_id: int, fetch=True):
        """Get a Fandom object.

        If the Fandom object does not exist in cache, it will fetch the name from the API.
        :param group_id: int
            The ID of the group to get/fetch a fandom name for.
        :param fetch: bool
            Whether to fetch from the API if not found in cache.
        :returns: :ref:`Fandom`
        """
        existing = _fandoms.get(group_id)
        if not existing:
            return await Fandom.fetch(group_id)
        return existing

    @staticmethod
    async def get_all():
        """
        Get all Fandom objects in cache.

        :returns: dict_values[:ref:`Fandom`]
            All Fandom objects from cache.
        """
        return _fandoms.values()

    @staticmethod
    async def fetch(group_id: int):
        """Fetch an updated Fandom object from the API.

        .. NOTE::: Fandom objects are added to cache on creation.

        :param group_id: int
            The group's ID to fetch a fandom for.
        :returns: :ref:`Fandom`
        """
        return await internal_fetch(
            obj=Fandom,
            request={
                "route": "fandom/$group_id",
                "group_id": group_id,
                "method": "GET",
            },
        )

    @staticmethod
    async def fetch_all():
        """Fetch all fandoms.

        .. NOTE::: Fandom objects are added to cache on creation.
        """
        return await internal_fetch_all(
            obj=Fandom, request={"route": "fandom/", "method": "GET"}
        )


_fandoms: Dict[int, Fandom] = dict()
