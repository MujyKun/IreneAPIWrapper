from typing import Union, List, Optional, Dict

from IreneAPIWrapper.sections import outer
from . import CallBack, Access, AbstractModel, internal_fetch, internal_fetch_all, MediaSource


class BloodType(AbstractModel):
    def __init__(self, blood_id, name):
        super(BloodType, self).__init__()
        self.id = blood_id
        self.name = name
        _blood_types[self.id] = self

    @staticmethod
    async def create(*args, **kwargs):
        blood_id = kwargs.get("bloodid")
        name = kwargs.get("name")

        return BloodType(blood_id, name)

    @staticmethod
    async def get(blood_id: int, fetch=True):
        """Get a BloodType object.

        If the BloodType object does not exist in cache, it will fetch the name from the API.
        :param blood_id: (int) The ID of the name to get/fetch.
        :param fetch: (bool) Whether to fetch from the API if not found in cache.
        """
        existing = _blood_types.get(blood_id)
        if not existing and fetch:
            return await BloodType.fetch(blood_id)
        return existing

    @staticmethod
    async def fetch(blood_id: int):
        """Fetch an updated BloodType object from the API.

        # NOTE: BloodType objects are added to cache on creation.

        :param blood_id: (int) The blood's ID to fetch.
        """
        return await internal_fetch(obj=BloodType, request={
            'route': 'bloodtype/$blood_id',
            'blood_id': blood_id,
            'method': 'GET'}
        )

    @staticmethod
    async def fetch_all():
        """Fetch all blood types.

        # NOTE: BloodType objects are added to cache on creation.
        """
        return await internal_fetch_all(obj=BloodType, request={
            'route': 'bloodtype/',
            'method': 'GET'}
        )


_blood_types: Dict[int, BloodType] = dict()
