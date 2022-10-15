from typing import Union, List, Optional, Dict

from IreneAPIWrapper.sections import outer
from . import (
    CallBack,
    Access,
    AbstractModel,
    internal_fetch,
    internal_fetch_all,
    MediaSource,
    Position,
    Person,
    Group,
    internal_delete,
    internal_insert,
)


class Affiliation(AbstractModel):
    r"""Represents the connection between a Person and Group object.

    An Affiliation object inherits from :ref:`AbstractModel`.

    Parameters
    ----------
    affiliation_id: int
        The Affiliation id.
    person: :ref:`Person`
        The person that is affiliated with a Group.
    group: :ref:`Group`
        The group that the Person is affiliated with.
    positions: Optional[List[:ref:`Position`]]
        The positions that the Person has in the Group.
    stage_name: str
        Exclusive name of the Person when they are in the Group.

    Attributes
    ----------
    id: int
        The Affiliation id.
    person: :ref:`Person`
        The person that is affiliated with a Group.
    group: :ref:`Group`
        The group that the Person is affiliated with.
    positions: List[:ref:`Position`]
        The positions that the Person has in the Group.
    stage_name: str
        Exclusive name of the Person when they are in the Group.

    """

    def __init__(
        self,
        affiliation_id: int,
        person: Person,
        group: Group,
        positions: Optional[List[Position]],
        stage_name: str,
    ):
        super(Affiliation, self).__init__(affiliation_id)
        self.person: Person = person
        self.group: Group = group
        self.positions: Optional[List[Position]] = positions
        self.stage_name: str = stage_name

        if not _affiliations.get(self.id):
            # we need to make sure not to override the current object in cache.
            _affiliations[self.id] = self

    @staticmethod
    def priority():
        return 2

    async def get_card(self, markdown=False, extra=True):
        card_data = []
        if self.id:
            card_data.append(f"Aff ID: {self.id}")
        if self.stage_name:
            card_data.append(f"Stage Name: {self.stage_name}")

        if not extra:
            return card_data

        if self.group:
            card_data.append(await self.group.get_card(markdown=markdown, extra=False)
            )
        if self.person:
            card_data.append(await self.person.get_card(markdown=markdown, extra=False))

        return card_data

    def __str__(self):
        return (
            f"Aff {self.id} - Person: {self.stage_name} [{self.person.id}] - Group: {str(self.group)} "
            f"[{self.group.id}]"
        )

    @staticmethod
    async def create(*args, **kwargs):
        """
        Create an Affiliation object.

        :returns: :ref:`Affiliation`
        """
        affiliation_id = kwargs.get("affiliationid")

        person_id = kwargs.get("personid")
        person = await Person.get(person_id)

        group_id = kwargs.get("groupid")
        group = await Group.get(group_id)

        position_ids = kwargs.get("positionids")
        positions = (
            []
            if not position_ids
            else [await Position.get(position_id) for position_id in position_ids]
        )

        stage_name = kwargs.get("stagename")

        Affiliation(affiliation_id, person, group, positions, stage_name)

        # This is a hacky method. The affiliation lists are checked for objects with the same ID and will remove them.
        # Then we add the new cached object.
        obj_in_cache = _affiliations[affiliation_id]
        if obj_in_cache in person.affiliations:
            person.affiliations.remove(obj_in_cache)
        if obj_in_cache in group.affiliations:
            group.affiliations.remove(obj_in_cache)

        # Add the current Affiliation to the Person and Group objects.
        person.affiliations.append(obj_in_cache)
        group.affiliations.append(obj_in_cache)

        return _affiliations[affiliation_id]

    async def delete(self) -> None:
        """
        Delete the Affiliation object from the database and remove it from cache.

        :returns: None
        """
        await internal_delete(
            self,
            request={
                "route": "affiliation/$affiliation_id",
                "affiliation_id": self.id,
                "method": "DELETE",
            },
        )
        await self._remove_from_cache()

    async def _remove_from_cache(self) -> None:
        """
        Remove the Affiliation object from cache.

        :returns: None
        """
        _affiliations.pop(self.id)

    @staticmethod
    async def insert(
        person_id: int, group_id: int, position_ids: List[int], stage_name: str
    ) -> bool:
        """
        Insert a new affiliation into the database.

        :param person_id: int
            The person id to affiliate with a Group.
        :param group_id: int
            The group id that is affiliated with a Person.
        :param position_ids: List[:ref:`int`]
            The Positions the Person has in the Group.
        :param stage_name: str
            The exclusive name of the Person in the Group.
        :return: bool
            Whether the affiliation was added to the existing objects as well as inserted into the DB.
        """
        callback = await internal_insert(
            request={
                "route": "affiliation",
                "person_id": person_id,
                "group_id": group_id,
                "position_ids": position_ids,
                "stage_name": stage_name,
                "method": "POST",
            }
        )
        results = callback.response.get("results")
        if not results:
            return False

        # TODO: Confirm the correct return is t_affiliation_id
        affiliation = await Affiliation.fetch(callback.response["t_affiliation_id"])

        group = await Group.get(group_id, fetch=False)
        person = await Person.get(person_id, fetch=False)
        if group:
            group.affiliations.append(affiliation)
        if person:
            person.affiliations.append(affiliation)
        return True

    @staticmethod
    async def get(affiliation_id: int, fetch=True):
        """Get an Affiliation object.

        If the Affiliation object does not exist in cache, it will fetch the name from the API.
        :param affiliation_id: int
            The ID of the affiliation to get/fetch.
        :param fetch: bool
            Whether to fetch from the API if not found in cache.
        :returns: Optional[:ref:`Affiliation`]
            The affiliation object requested.
        """
        existing = _affiliations.get(affiliation_id)
        if not existing and fetch:
            return await Affiliation.fetch(affiliation_id)
        return existing

    @staticmethod
    async def get_all():
        """
        Get all Affiliation objects in cache.

        :returns: dict_values[:ref:`Affiliation`]
            All Affiliation objects from cache.
        """
        return _affiliations.values()

    @staticmethod
    async def fetch(affiliation_id: int):
        """Fetch an updated affiliation object from the API.

        .. NOTE:: affiliation objects are added to cache on creation.

        :param affiliation_id: int
            The affiliation's ID to fetch.
        :returns: Optional[:ref:`Affiliation`]
            The affiliation object requested.
        """
        return await internal_fetch(
            obj=Affiliation,
            request={
                "route": "affiliation/$affiliation_id",
                "affiliation_id": affiliation_id,
                "method": "GET",
            },
        )

    @staticmethod
    async def fetch_all():
        """Fetch all affiliations.

        .. NOTE:: affiliation objects are added to cache on creation.
        """
        return await internal_fetch_all(
            obj=Affiliation, request={"route": "affiliation", "method": "GET"}
        )


_affiliations: Dict[int, Affiliation] = dict()
