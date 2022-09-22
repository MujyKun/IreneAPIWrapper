from typing import Union, List, Optional, Dict, TYPE_CHECKING

from IreneAPIWrapper.sections import outer
from . import (
    CallBack,
    Access,
    Date,
    AbstractModel,
    internal_fetch,
    internal_fetch_all,
    Name,
    Display,
    Social,
    Location,
    BloodType,
    Tag,
    internal_delete,
    internal_insert,
)

if TYPE_CHECKING:
    from . import Affiliation, PersonAlias


class Person(AbstractModel):

    r"""Represents a Person (or a living entity).

    A Person object inherits from :ref:`AbstractModel`.

    Note: Several Person objects will be referenced as "persons" and not "people".

    Parameters
    ----------
    person_id: int
        The person's ID.
    date: :ref:`Date`
        Birth/Death date of a person.
    name: :ref:`Name`
        The official Name of the person.
    former_name: :ref:`Name`
        The former Name object of the person.
    display: :ref:`Display`
        The avatar/banner displays for the person.
    social: :ref:`Social`
        All social media references for the person.
    location: :ref:`Location`
        The birth location of the person.
    blood_type: :ref:`BloodType`
        The blood type of the person.
    gender: str
        The gender of the person.
    description: str
        A general overview of the person.
    height: int
        The height of the person in centimeters (cm)
    call_count: int
        The amount of times the person has been called. (Increment determined by client side and not from the API)
    media_count: int
        The media a person has.
    tags: List[:ref:`Tag`]
        The tags associated with the person.
    aliases: List[:ref:`PersonAlias`]
        The aliases associated with the person.

    Attributes
    ----------
    id: int
        The person's ID.
    date: :ref:`Date`
        Birth/Death date of a person.
    name: :ref:`Name`
        The official Name of the person.
    former_name: :ref:`Name`
        The former Name object of the person.
    display: :ref:`Display`
        The avatar/banner displays for the person.
    social: :ref:`Social`
        All social media references for the person.
    location: :ref:`Location`
        The birth location of the person.
    blood_type: :ref:`BloodType`
        The blood type of the person.
    gender: str
        The gender of the person.
    description: str
        A general overview of the person.
    height: int
        The height of the person in centimeters (cm)
    call_count: int
        The amount of times the person has been called. (Increment determined by client side and not from the API)
    media_count: int
        The media a person has.
    tags: List[:ref:`Tag`]
        The tags associated with the person.
    aliases: List[:ref:`PersonAlias`]
        The aliases associated with the person.
    affiliations: List[:ref:`Affiliation`]
        A list of :ref:`Affiliation` objects between the :ref:`Person` and the :ref:`Group` objects they are in.
    """
    def __init__(
        self,
        person_id,
        date,
        name,
        former_name,
        display,
        social,
        location,
        blood_type,
        gender,
        description,
        height,
        call_count,
        media_count,
        tags,
        aliases,
    ):
        super(Person, self).__init__(person_id)
        self.date: Date = date
        self.name: Name = name
        self.former_name: Name = former_name
        self.display: Display = display
        self.social: Social = social
        self.location: Location = location
        self.blood_type: BloodType = blood_type
        self.gender: str = gender
        self.description: str = description
        self.height: int = height
        self.call_count: int = call_count
        self.media_count: int = media_count or 0
        self.tags: List[Tag] = tags
        self.aliases: List[PersonAlias] = aliases
        self.affiliations: List[Affiliation] = []

        if not _persons.get(self.id):
            _persons[self.id] = self

    @staticmethod
    def priority():
        return 1

    async def get_card(self, markdown=False, extra=True):
        card_data = []
        if self.id:
            card_data.append(f"Person ID: {self.id}")
        if self.name:
            card_data.append(f"Name: {str(self.name)}")
        if self.description:
            card_data.append(f"Description: {self.description}")

        if not extra:
            return card_data

        if self.former_name:
            card_data.append(f"Former Name: {str(self.former_name)}")
        if self.call_count:
            card_data.append(f"Called: {self.call_count} time(s).")
        if self.height:
            card_data.append(f"Height: {self.height}cm")
        if self.blood_type:
            card_data.append(f"BloodType: {self.blood_type.name}")
        if self.location:
            card_data.append(f"Birth Location: {str(self.location)}")
        if self.gender:
            card_data.append(f"Gender: {self.gender}")
        if self.date:
            date_card = await self.date.get_card(markdown=markdown)
            [card_data.append(info) for info in date_card]
        if self.display:
            display_card = await self.display.get_card(markdown=markdown)
            [card_data.append(info) for info in display_card]
        if self.social:
            social_card = await self.social.get_card(markdown=markdown)
            [card_data.append(info) for info in social_card]
        if self.tags:
            tags = ", ".join([str(tag) for tag in self.tags])
            card_data.append(f"Tags: {tags}")
        if self.aliases:
            aliases = ", ".join([str(alias) for alias in self.aliases])
            card_data.append(f"Aliases: {aliases}")
        if self.affiliations:
            affiliations = "\n".join([str(aff) for aff in self.affiliations])
            card_data.append(f"Affiliations:\n{affiliations}")
        return card_data

    @staticmethod
    async def create(*args, **kwargs):
        """Create a Person object."""
        person_id = kwargs.get("personid")

        date_id = kwargs.get("dateid")
        date = await Date.get(date_id)

        name_id = kwargs.get("nameid")
        name = await Name.get(name_id)

        former_name_id = kwargs.get("nameid")
        former_name = await Name.get(former_name_id)

        display_id = kwargs.get("displayid")
        display: Display = await Display.get(display_id)

        social_id = kwargs.get("socialid")
        social: Social = await Social.get(social_id)

        location_id = kwargs.get("locationid")
        location: Location = await Location.get(location_id)

        blood_id = kwargs.get("bloodid")
        blood_type: BloodType = await BloodType.get(blood_id)

        gender = kwargs.get("gender")

        description = kwargs.get("description")

        height = kwargs.get("height")

        call_count = kwargs.get("callcount")
        media_count = kwargs.get("mediacount")

        tag_ids = kwargs.get("tagids")
        tags = [] if not tag_ids else [await Tag.get(tag_id) for tag_id in tag_ids]

        alias_ids = kwargs.get("aliasids")

        # avoiding circular import when updating cache on PersonAlias insertions.
        from . import PersonAlias

        aliases = (
            []
            if not alias_ids
            else [await PersonAlias.get(alias_id) for alias_id in alias_ids]
        )

        Person(
            person_id,
            date,
            name,
            former_name,
            display,
            social,
            location,
            blood_type,
            gender,
            description,
            height,
            call_count,
            media_count,
            tags,
            aliases,
        )
        return _persons[person_id]

    def __str__(self):
        return str(self.name)

    async def get_aliases_as_strings(self) -> List:
        return [alias.name for alias in self.aliases]

    async def delete(self) -> None:
        """
        Delete the Person object from the database and remove it from cache.

        :returns: None
        """
        await internal_delete(
            self,
            request={
                "route": "person/$person_id",
                "person_id": self.id,
                "method": "DELETE",
            },
        )
        await self._remove_from_cache()

    async def _remove_from_cache(self) -> None:
        """
        Remove the Person object from cache.

        :returns: None
        """
        _persons.pop(self.id)

    @staticmethod
    async def insert(
        date_id,
        name_id,
        former_name_id,
        gender,
        description,
        height,
        display_id,
        social_id,
        location_id,
        tag_ids,
        blood_id,
        call_count,
    ) -> None:
        r"""
        Insert a new person into the database.


        Parameters
        ----------
        date_id: int
            The :ref:`Date` ID of the person.
        name_id: int
            The official :ref:`Name` ID of the person.
        former_name_id: int
            The former :ref:`Name` ID of the person.
        gender: str
            The gender of the person.
        description: str
            An overview of the person.
        height: int
            The height of the person in centimeters (cm).
        display_id: int
            The :ref:`Display` ID of the person.
        social_id: int
            The :ref:`Social` ID of the person.
        location_id: int
            The Birth :ref:`Location` ID of the person.
        tag_ids: List[int]
            A list of :ref:`Tag` IDs of the person.
        blood_id: int
            The :ref:`BloodType` ID of the person.
        call_count: int
            The number of times the person has been called.

        :returns: None
        """
        await internal_insert(
            request={
                "route": "person",
                "date_id": date_id,
                "name_id": name_id,
                "former_name_id": former_name_id,
                "gender": gender,
                "description": description,
                "height": height,
                "display_id": display_id,
                "social_id": social_id,
                "location_id": location_id,
                "tag_ids": tag_ids,
                "blood_id": blood_id,
                "call_count": call_count,
                "method": "POST",
            }
        )

    @staticmethod
    async def get(person_id: int, fetch=True):
        """Get a Person object.

        If the Person object does not exist in cache, it will fetch the person from the API.
        :param person_id: int
            The ID of the person to get/fetch.
        :param fetch: bool
            Whether to fetch from the API if not found in cache.
        :returns: :ref:`Person`
        """
        existing = _persons.get(person_id)
        if not existing and fetch:
            return await Person.fetch(person_id)
        return existing

    @staticmethod
    async def get_all():
        """
        Get all Person objects in cache.

        :returns: dict_values[:ref:`Person`]
            All Person objects from cache.
        """
        return _persons.values()

    @staticmethod
    async def fetch(person_id: int):
        """Fetch an updated Person object from the API.

        .. NOTE::: Person objects are added to cache on creation.

        :param person_id: int
            The person's ID to fetch.
        :returns: :ref:`Person`
        """
        return await internal_fetch(
            obj=Person,
            request={
                "route": "person/$person_id",
                "person_id": person_id,
                "method": "GET",
            },
        )

    @staticmethod
    async def fetch_all():
        """Fetch all persons.

        .. NOTE::: Person objects are added to cache on creation.
        """
        return await internal_fetch_all(
            obj=Person, request={"route": "person/", "method": "GET"}
        )


_persons: Dict[int, Person] = dict()
