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


class Location(AbstractModel):
    r"""Represents a location.

    A Location object inherits from :ref:`AbstractModel`.

    Parameters
    ----------
    location_id: int
        The Affiliation id.
    country: str
        The country's name.
    city: str
        The city's name.

    Attributes
    ----------
    id: int
        The Location id.
    country: str
        The country's name.
    city: str
        The city's name.

    """

    def __init__(self, location_id, country, city):
        super(Location, self).__init__(location_id)
        self.country = country
        self.city = city
        if not _locations.get(self.id):
            _locations[self.id] = self

    def __str__(self):
        return f"{self.country} - {self.country}"

    @staticmethod
    async def create(*args, **kwargs):
        """
        Create a Location object.

        :returns: :ref:`Location`
        """
        location_id = kwargs.get("locationid")
        country = kwargs.get("country")
        city = kwargs.get("city")

        Location(location_id, country, city)
        return _locations[location_id]

    async def delete(self) -> None:
        """
        Delete the Location object from the database and remove it from cache.

        :returns: None
        """
        await internal_delete(
            self,
            request={
                "route": "location/$location_id",
                "location_id": self.id,
                "method": "DELETE",
            },
        )
        await self._remove_from_cache()

    async def _remove_from_cache(self) -> None:
        """
        Remove the Location object from cache.

        :returns: None
        """
        _locations.pop(self.id)

    @staticmethod
    async def insert(country, city) -> None:
        """
        Insert a new location into the database.

        :param country: The country's name.
        :param city: The city's name.
        :returns: None
        """
        await internal_insert(
            request={
                "route": "location",
                "country": country,
                "city": city,
                "method": "POST",
            }
        )

    @staticmethod
    async def get(location_id: int, fetch=True):
        """Get a Location object.

        If the Location object does not exist in cache, it will fetch the name from the API.
        :param location_id: int
            The ID of the location to get/fetch.
        :param fetch: bool
            Whether to fetch from the API if not found in cache.
        """
        existing = _locations.get(location_id)
        if not existing and fetch:
            return await Location.fetch(location_id)
        return existing

    @staticmethod
    async def get_all():
        """
        Get all Location objects in cache.

        :returns: dict_values[:ref:`Location`]
            All Location objects from cache.
        """
        return _locations.values()

    @staticmethod
    async def fetch(location_id: int):
        """Fetch an updated Location object from the API.

        .. NOTE::: Location objects are added to cache on creation.

        :param location_id: int
            The location's ID to fetch.
        """
        return await internal_fetch(
            obj=Location,
            request={
                "route": "location/$location_id",
                "location_id": location_id,
                "method": "GET",
            },
        )

    @staticmethod
    async def fetch_all():
        """Fetch all locations.

        .. NOTE::: Location objects are added to cache on creation.
        """
        return await internal_fetch_all(
            obj=Location, request={"route": "location/", "method": "GET"}
        )


_locations: Dict[int, Location] = dict()
