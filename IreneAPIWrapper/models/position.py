from typing import Union, List, Optional, Dict

from IreneAPIWrapper.sections import outer
from . import CallBack, Access, AbstractModel, internal_fetch, internal_fetch_all, MediaSource


class Position(AbstractModel):
    def __init__(self, position_id, name):
        super(Position, self).__init__()
        self.id = position_id
        self.name = name
        _positions[self.id] = self

    @staticmethod
    async def create(*args, **kwargs):
        position_id = kwargs.get("positionid")
        name = kwargs.get("name")

        return Position(position_id, name)

    @staticmethod
    async def get(position_id: int, fetch=True):
        """Get a Position object.

        If the Position object does not exist in cache, it will fetch the name from the API.
        :param position_id: (int) The ID of the name to get/fetch.
        :param fetch: (bool) Whether to fetch from the API if not found in cache.
        """
        existing = _positions.get(position_id)
        if not existing:
            return await Position.fetch(position_id)
        return existing

    @staticmethod
    async def fetch(position_id: int):
        """Fetch an updated Position object from the API.

        # NOTE: Position objects are added to cache on creation.

        :param position_id: (int) The position's ID to fetch.
        """
        return await internal_fetch(obj=Position, request={
            'route': 'position/$position_id',
            'position_id': position_id,
            'method': 'GET'}
        )

    @staticmethod
    async def fetch_all():
        """Fetch all positions.

        # NOTE: Position objects are added to cache on creation.
        """
        return await internal_fetch_all(obj=Position, request={
            'route': 'position/',
            'method': 'GET'}
        )


_positions: Dict[int, Position] = dict()
