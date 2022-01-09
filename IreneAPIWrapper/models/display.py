from typing import Union, List, Optional, Dict

from IreneAPIWrapper.sections import outer
from . import CallBack, Access, AbstractModel, internal_fetch, internal_fetch_all, MediaSource


class Display(AbstractModel):
    def __init__(self, *args, **kwargs):
        super(Display, self).__init__()
        self.id = kwargs.get("displayid")
        self.avatar: MediaSource = MediaSource(kwargs.get("avatar"))
        self.banner: MediaSource = MediaSource(kwargs.get("banner"))
        _displays[self.id] = self

    @staticmethod
    async def create(*args, **kwargs):
        # TODO: Create
        return Display(*args)

    @staticmethod
    async def get(display_id: int, fetch=True):
        """Get a Display object.

        If the Display object does not exist in cache, it will fetch the name from the API.
        :param display_id: (int) The ID of the name to get/fetch.
        :param fetch: (bool) Whether to fetch from the API if not found in cache.
        """
        existing = _displays.get(display_id)
        if not existing:
            return await Display.fetch(display_id)
        return existing

    @staticmethod
    async def fetch(display_id: int):
        """Fetch an updated Display object from the API.

        # NOTE: Display objects are added to cache on creation.

        :param display_id: (int) The display's ID to fetch.
        """
        return await internal_fetch(obj=Display, request={
            'route': 'display/$display_id',
            'display_id': display_id,
            'method': 'GET'}
        )

    @staticmethod
    async def fetch_all():
        """Fetch all displays.

        # NOTE: Display objects are added to cache on creation.
        """
        return await internal_fetch_all(obj=Display, request={
            'route': 'display/',
            'method': 'GET'}
        )


_displays: Dict[int, Display] = dict()
