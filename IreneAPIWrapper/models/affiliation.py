from typing import Union, List, Optional, Dict

from IreneAPIWrapper.sections import outer
from . import CallBack, Access, AbstractModel, internal_fetch, internal_fetch_all, MediaSource, Position, Person, Group


class Affiliation(AbstractModel):
    def __init__(self, affiliation_id, person, group, positions, stage_name):
        super(Affiliation, self).__init__()
        self.id = affiliation_id
        self.person: Person = person
        self.group: Group = group
        self.positions: Position = positions
        self.stage_name: str = stage_name
        _affiliations[self.id] = self

    @staticmethod
    async def create(*args, **kwargs):
        affiliation_id = kwargs.get("affiliationid")

        person_id = kwargs.get("personid")
        person = await Person.get(person_id)

        group_id = kwargs.get("groupid")
        group = await Group.get(group_id)

        position_ids = kwargs.get("positionids")
        positions = [] if not position_ids else [await Position.get(position_id) for position_id in position_ids]

        stage_name = kwargs.get("stagename")

        affiliation_args = {affiliation_id, person, group, positions, stage_name}

        aff_obj = Affiliation(*affiliation_args)
        person.affiliations.append(aff_obj)
        group.affiliations.append(aff_obj)

        return aff_obj

    @staticmethod
    async def get(affiliation_id: int, fetch=True):
        """Get an Affiliation object.

        If the Affiliation object does not exist in cache, it will fetch the name from the API.
        :param affiliation_id: (int) The ID of the name to get/fetch.
        :param fetch: (bool) Whether to fetch from the API if not found in cache.
        """
        existing = _affiliations.get(affiliation_id)
        if not existing and fetch:
            return await Affiliation.fetch(affiliation_id)
        return existing

    @staticmethod
    async def fetch(affiliation_id: int):
        """Fetch an updated affiliation object from the API.

        # NOTE: affiliation objects are added to cache on creation.

        :param affiliation_id: (int) The affiliation's ID to fetch.
        """
        return await internal_fetch(obj=Affiliation, request={
            'route': 'affiliation/$affiliation_id',
            'affiliation_id': affiliation_id,
            'method': 'GET'}
        )

    @staticmethod
    async def fetch_all():
        """Fetch all affiliations.

        # NOTE: affiliation objects are added to cache on creation.
        """
        return await internal_fetch_all(obj=Affiliation, request={
            'route': 'affiliation/',
            'method': 'GET'}
        )


_affiliations: Dict[int, Affiliation] = dict()
