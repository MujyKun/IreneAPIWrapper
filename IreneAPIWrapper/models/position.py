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


class Position(AbstractModel):
    r"""Represents a position or status.

    A Position object inherits from :ref:`AbstractModel`.

    Parameters
    ----------
    position_id: int
        The Position id.
    name: str
        The position's name.

    Attributes
    ----------
    id: int
        The Position id.
    name: str
        The position's name.
    """

    def __init__(self, position_id, name):
        super(Position, self).__init__(position_id)
        self.name = name
        if not _positions.get(self.id):
            _positions[self.id] = self

    @staticmethod
    async def create(*args, **kwargs):
        """
        Create a Position object.

        :returns: :ref:`Position`
        """
        position_id = kwargs.get("positionid")
        name = kwargs.get("name")

        Position(position_id, name)
        return _positions[position_id]

    async def delete(self) -> None:
        """
        Delete the Position object from the database and remove it from cache.

        :returns: None
        """
        await internal_delete(
            self,
            request={
                "route": "position/$position_id",
                "position_id": self.id,
                "method": "DELETE",
            },
        )
        await self._remove_from_cache()

    async def _remove_from_cache(self) -> None:
        """
        Remove the Position object from cache.

        :returns: None
        """
        _positions.pop(self.id)

    @staticmethod
    async def insert(name) -> None:
        """
        Insert a new position into the database.

        :param name: str
            The position name.
        :returns: None
        """
        await internal_insert(
            request={"route": "position", "position_name": name, "method": "POST"}
        )

    @staticmethod
    async def get(position_id: int, fetch=True):
        """Get a Position object.

        If the Position object does not exist in cache, it will fetch the name from the API.
        :param position_id: int
            The ID of the name to get/fetch.
        :param fetch: bool
            Whether to fetch from the API if not found in cache.
        :returns: :ref:`Position`
        """
        existing = _positions.get(position_id)
        if not existing:
            return await Position.fetch(position_id)
        return existing

    @staticmethod
    async def get_all():
        """
        Get all Position objects in cache.

        :returns: dict_values[:ref:`Position`]
            All Position objects from cache.
        """
        return _positions.values()

    @staticmethod
    async def fetch(position_id: int):
        """Fetch an updated Position object from the API.

        .. NOTE::: Position objects are added to cache on creation.

        :param position_id: int
            The position's ID to fetch.
        :returns: :ref:`Position`
        """
        return await internal_fetch(
            obj=Position,
            request={
                "route": "position/$position_id",
                "position_id": position_id,
                "method": "GET",
            },
        )

    @staticmethod
    async def fetch_all():
        """Fetch all positions.

        .. NOTE::: Position objects are added to cache on creation.
        """
        return await internal_fetch_all(
            obj=Position, request={"route": "position/", "method": "GET"}
        )


_positions: Dict[int, Position] = dict()
