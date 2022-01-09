from typing import Union, List, Optional, Dict

from IreneAPIWrapper.sections import outer
from . import CallBack, Access, AbstractModel, internal_fetch, internal_fetch_all, MediaSource


class Affiliation(AbstractModel):
    def __init__(self, *args, **kwargs):
        super(Affiliation, self).__init__()
        self.id = kwargs.get("affiliationid")
        self.avatar: MediaSource = MediaSource(kwargs.get("avatar"))
        self.banner: MediaSource = MediaSource(kwargs.get("banner"))
        _affiliations[self.id] = self

    async def create(self, *args, **kwargs):
        # TODO : create
        return Affiliation(*args)

    @staticmethod
    async def get(affiliation_id: int):
        """Get an Affiliation object.

        If the Affiliation object does not exist in cache, it will fetch the name from the API.
        :param affiliation_id: (int) The ID of the name to get/fetch.
        """
        existing_person = _affiliations.get(affiliation_id)
        if not existing_person:
            return await Affiliation.fetch(affiliation_id)

    @staticmethod
    async def fetch(affiliation_id: int):
        """Fetch an updated affiliation object from the API.

        # NOTE: affiliation objects are added to cache on creation.

        :param affiliation_id: (int) The affiliation's ID to fetch.
        """
        return internal_fetch(obj=Affiliation, request={
            'route': 'affiliation/$affiliation_id',
            'affiliation_id': affiliation_id,
            'method': 'GET'}
        )

    @staticmethod
    async def fetch_all():
        """Fetch all affiliations.

        # NOTE: affiliation objects are added to cache on creation.
        """
        return internal_fetch_all(obj=Affiliation, request={
            'route': 'affiliation/',
            'method': 'GET'}
        )


_affiliations: Dict[int, Affiliation] = dict()
