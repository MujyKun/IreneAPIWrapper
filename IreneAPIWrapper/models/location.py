from typing import Union, List, Optional, Dict

from IreneAPIWrapper.sections import outer
from . import CallBack, Access, AbstractModel, internal_fetch, internal_fetch_all, MediaSource


class Location(AbstractModel):
    def __init__(self, location_id, country, city):
        super(Location, self).__init__()
        self.id = location_id
        self.country = country
        self.city = city
        _locations[self.id] = self

    @staticmethod
    async def create(*args, **kwargs):
        location_id = kwargs.get("locationid")
        country = kwargs.get("country")
        city = kwargs.get("city")

        return Location(location_id, country, city)

    @staticmethod
    async def get(location_id: int, fetch=True):
        """Get a Location object.

        If the Location object does not exist in cache, it will fetch the name from the API.
        :param location_id: (int) The ID of the name to get/fetch.
        :param fetch: (bool) Whether to fetch from the API if not found in cache.
        """
        existing = _locations.get(location_id)
        if not existing and fetch:
            return await Location.fetch(location_id)
        return existing

    @staticmethod
    async def fetch(location_id: int):
        """Fetch an updated Location object from the API.

        # NOTE: Location objects are added to cache on creation.

        :param location_id: (int) The location's ID to fetch.
        """
        return await internal_fetch(obj=Location, request={
            'route': 'location/$location_id',
            'location_id': location_id,
            'method': 'GET'}
        )

    @staticmethod
    async def fetch_all():
        """Fetch all locations.

        # NOTE: Location objects are added to cache on creation.
        """
        return await internal_fetch_all(obj=Location, request={
            'route': 'location/',
            'method': 'GET'}
        )


_locations: Dict[int, Location] = dict()
