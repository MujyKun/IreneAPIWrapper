from typing import Union, List, Optional, Dict

from IreneAPIWrapper.sections import outer
from . import CallBack, Access, AbstractModel, internal_fetch, internal_fetch_all,\
    internal_insert, internal_delete


class Date(AbstractModel):
    r"""Represents a starting and end date of an entity.

    A Date object inherits from :ref:`AbstractModel`.

    Parameters
    ----------
    date_id: int
        The Date ID.
    start_date: str
        The start date.
    end_date: str
        The end date.


    Attributes
    ----------
    id: int
        The Date id.
    start: str
        The start date.
    end: str
        The end date.

    """
    def __init__(self, date_id: int, start_date: str, end_date: str, *args, **kwargs):
        super(Date, self).__init__(date_id)
        self.start: str = start_date
        self.end: str = end_date
        _dates[self.id] = self

    @staticmethod
    async def create(*args, **kwargs):
        """
        Create a Date object.

        :returns: :ref:`Date`
        """
        date_id = kwargs.get("dateid")
        start_date = kwargs.get("startdate")
        end_date = kwargs.get("enddate")

        return Date(date_id, start_date, end_date)

    async def delete(self) -> None:
        """Delete the Date object from the database and remove it from cache.

        :returns: None
        """
        await internal_delete(self, request={
            'route': 'date/$date_id',
            'date_id': self.id,
            'method': 'DELETE'
        })

    async def _remove_from_cache(self) -> None:
        """Remove the Date object from cache.

        :returns: None
        """
        _dates.pop(self.id)

    @staticmethod
    async def insert(start_date, end_date=None) -> None:
        """
        Insert a new date into the database.

        :param start_date: The start date.
        :param end_date: The end date if there is one.
        :returns: None
        """
        await internal_insert(request={
            'route': 'date',
            'start_date': start_date,
            'end_date': end_date,
            'method': 'POST'
        })

    @staticmethod
    async def get(date_id: int, fetch=True):
        """Get a Date object.

        If the Date object does not exist in cache, it will fetch the date from the API.

        :param date_id: int
            The ID of the date to get/fetch.
        :param fetch: bool
            Whether to fetch from the API if not found in cache.
        :returns: Optional[:ref:`Date`]
            The date object requested.
        """
        existing = _dates.get(date_id)
        if not existing and fetch:
            return await Date.fetch(date_id)
        return existing

    @staticmethod
    async def get_all():
        """
        Get all Date objects in cache.

        :returns: dict_values[:ref:`Date`]
            All Date objects from cache.
        """
        return _dates.values()

    @staticmethod
    async def fetch(date_id: int):
        """Fetch an updated Date object from the API.

        .. NOTE::: Date objects are added to cache on creation.

        :param date_id: int
            The date's ID to fetch.
        :returns: Optional[:ref:`Date`]
            The date object requested.
        """
        return await internal_fetch(Date, request={
            'route': 'date/$date_id',
            'date_id': date_id,
            'method': 'GET'
        })

    @staticmethod
    async def fetch_all():
        """Fetch all dates.

        .. NOTE::: Date objects are added to cache on creation.
        """
        return await internal_fetch_all(obj=Date, request={
            'route': 'date/',
            'method': 'GET'
        })


_dates: Dict[int, Date] = dict()
