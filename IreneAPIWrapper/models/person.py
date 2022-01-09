from typing import Union, List, Optional, Dict, TYPE_CHECKING

from IreneAPIWrapper.sections import outer
from . import CallBack, Access, Date, AbstractModel, internal_fetch, internal_fetch_all, Name, Display, Social, \
    PersonAlias, Location, BloodType, Tag

if TYPE_CHECKING:
    from . import Affiliation


class Person(AbstractModel):
    def __init__(self, person_id, date, name, former_name, display, social, location, blood_type, gender,
                 description, height, call_count, tags, aliases):
        super(Person, self).__init__()
        self.id = person_id
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
        self.tags: List[Tag] = tags
        self.aliases: List[PersonAlias] = aliases
        self.affiliations: List[Affiliation] = []
        _persons[self.id] = self

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

        tag_ids = kwargs.get("tagids")
        tags = [] if not tag_ids else [await Tag.get(tag_id) for tag_id in tag_ids]

        alias_ids = kwargs.get("aliasids")
        aliases = [] if not alias_ids else [await PersonAlias.get(alias_id) for alias_id in alias_ids]

        return Person(person_id, date, name, former_name, display, social, location, blood_type, gender,
                      description, height, call_count, tags, aliases)

    @staticmethod
    async def get(person_id: int, fetch=True):
        """Get a Person object.

        If the Person object does not exist in cache, it will fetch the person from the API.
        :param person_id: (int) The ID of the person to get/fetch.
        :param fetch: (bool) Whether to fetch from the API if not found in cache.
        """
        existing = _persons.get(person_id)
        if not existing and fetch:
            return await Person.fetch(person_id)
        return existing

    @staticmethod
    async def fetch(person_id: int):
        """Fetch an updated Person object from the API.

        # NOTE: Person objects are added to cache on creation.

        :param person_id: (int) The person's ID to fetch.
        """
        return await internal_fetch(obj=Person, request={
            'route': 'person/$person_id',
            'person_id': person_id,
            'method': 'GET'}
            )

    @staticmethod
    async def fetch_all():
        """Fetch all persons.

        # NOTE: Person objects are added to cache on creation.
        """
        return await internal_fetch_all(obj=Person, request={
            'route': 'person/',
            'method': 'GET'}
                                  )


_persons: Dict[int, Person] = dict()
