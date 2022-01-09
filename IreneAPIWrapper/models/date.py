from typing import Union, List, Optional, Dict

from IreneAPIWrapper.sections import outer
from . import CallBack, Access, AbstractModel, internal_fetch, internal_fetch_all


class Date(AbstractModel):
    def __init__(self, *args, **kwargs):
        super(Date, self).__init__()
        self.id = kwargs.get("dateid")
        self.start: str = kwargs.get("startdate")
        self.end: str = kwargs.get("enddate")
        _dates[self.id] = self

    async def create(self, *args, **kwargs):
        # TODO: Create

        return Date(*args)

    @staticmethod
    async def get(date_id: int):
        """Get a Date object.

        If the Date object does not exist in cache, it will fetch the date from the API.
        :param date_id: (int) The ID of the date to get/fetch.
        """
        existing_person = _dates.get(date_id)
        if not existing_person:
            return await Date.fetch(date_id)

    @staticmethod
    async def fetch(date_id: int):
        """Fetch an updated Date object from the API.

        # NOTE: Date objects are added to cache on creation.

        :param date_id: (int) The date's ID to fetch.
        """

        callback = CallBack(request={
            'route': 'date/$date_id',
            'date_id': date_id,
            'method': 'GET'}
        )

        await outer.client.add_and_wait(callback)

        return Date(**callback.response["results"])

    @staticmethod
    async def fetch_all_dates(self):
        """Fetch all dates.

        # NOTE: Date objects are added to cache on creation.
        """
        callback = CallBack(request={
            'route': 'date/',
            'method': 'GET'}
        )

        await outer.client.add_and_wait(callback)

        if not callback.response["results"]:
            return []

        return [Date(**info) for info in callback.response["results"]]


_dates: Dict[int, Date] = dict()
