from typing import Union, List, Optional, Dict

from IreneAPIWrapper.sections import outer
from . import CallBack, Access, AbstractModel, internal_fetch, internal_fetch_all


class Name(AbstractModel):
    def __init__(self, *args, **kwargs):
        super(Name, self).__init__()
        self.id = kwargs.get("nameid")
        self.first: str = kwargs.get("firstname")
        self.last: str = kwargs.get("lastname")
        _names[self.id] = self

    @staticmethod
    async def get(name_id: int, fetch=True):
        """Get a Name object.

        If the Name object does not exist in cache, it will fetch the name from the API.
        :param name_id: (int) The ID of the name to get/fetch.
        :param fetch: (bool) Whether to fetch from the API if not found in cache.
        """
        existing = _names.get(name_id)
        if not existing and fetch:
            return await Name.fetch(name_id)
        return existing

    @staticmethod
    async def fetch(name_id: int):
        """Fetch an updated Name object from the API.

        # NOTE: Name objects are added to cache on creation.

        :param name_id: (int) The name's ID to fetch.
        """
        return await internal_fetch(obj=Name, request={
            'route': 'name/$name_id',
            'name_id': name_id,
            'method': 'GET'}
        )

    @staticmethod
    async def fetch_all():
        """Fetch all names.

        # NOTE: Name objects are added to cache on creation.
        """
        return await internal_fetch_all(obj=Name, request={
            'route': 'name/',
            'method': 'GET'}
        )


_names: Dict[int, Name] = dict()
