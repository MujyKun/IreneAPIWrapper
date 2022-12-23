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
    basic_call,
)


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

        if not _dates.get(self.id):
            _dates[self.id] = self

    async def get_card(self, markdown=False):
        card_data = []
        if self.start:
            card_data.append(f"Start Date: {self.start}")
        if self.end:
            card_data.append(f"End Date: {self.end}")
        return card_data

    @staticmethod
    async def create(*args, **kwargs):
        """
        Create a Date object.

        :returns: :ref:`Date`
        """
        date_id = kwargs.get("dateid")
        start_date = kwargs.get("startdate")
        end_date = kwargs.get("enddate")
        Date(date_id, start_date, end_date)
        return _dates[date_id]

    async def delete(self) -> None:
        """Delete the Date object from the database and remove it from cache.

        :returns: None
        """
        await internal_delete(
            self,
            request={"route": "date/$date_id", "date_id": self.id, "method": "DELETE"},
        )
        await self._remove_from_cache()

    async def update_end_date(self, end_date) -> None:
        """
        Update the end date.

        :param end_date: Union[str, Datetime]
            Datetime or string object in '%Y-%m-%d %H:%M:%S.%f' format (equivalent to datetime.now()).
            Is the end date.
        :return: None
        """
        await basic_call(
            request={
                "route": "date/$date_id",
                "date_id": self.id,
                "end_date": str(end_date),
                "method": "PUT",
            }
        )

    async def _remove_from_cache(self) -> None:
        """Remove the Date object from cache.

        :returns: None
        """
        _dates.pop(self.id)

    @staticmethod
    async def insert(start_date, end_date=None) -> int:
        """
        Insert a new date into the database.

        :param start_date: Union[str, Datetime]
            Datetime or string object in '%Y-%m-%d %H:%M:%S.%f' format (equivalent to datetime.now()).
            Is the start date.
        :param end_date: Union[str, Datetime]
            Datetime or string object in '%Y-%m-%d %H:%M:%S.%f' format (equivalent to datetime.now()).
            Is the end date.
        :returns: int
            The Date id
        """
        callback = await internal_insert(
            request={
                "route": "date",
                "start_date": str(start_date),
                "end_date": str(end_date) if end_date else end_date,
                "method": "POST",
            }
        )
        results = callback.response.get("results")
        if not results:
            return False

        return results["adddate"]

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
        if not date_id:
            return None
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
        return await internal_fetch(
            Date,
            request={"route": "date/$date_id", "date_id": date_id, "method": "GET"},
        )

    @staticmethod
    async def fetch_all():
        """Fetch all dates.

        .. NOTE::: Date objects are added to cache on creation.
        """
        return await internal_fetch_all(
            obj=Date, request={"route": "date/", "method": "GET"}
        )


_dates: Dict[int, Date] = dict()
