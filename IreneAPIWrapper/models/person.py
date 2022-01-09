from typing import Union, List, Optional, Dict

from IreneAPIWrapper.sections import outer
from . import CallBack, Access, Date, AbstractModel, internal_fetch, internal_fetch_all, Name


class Person(AbstractModel):
    def __init__(self, person_id, date, name, former_name, display, social, location, bloodtype,
                 gender, description, height, call_count, tags, **kwargs):
        super(Person, self).__init__()
        self.id: int = kwargs.get("personid")
        self.date: Date = Date.get(kwargs.get("dateid"))
        self.birth_date: str = kwargs.get("startdate")
        self.death_date: str = kwargs.get("enddate")
        self.first_name: str = kwargs.get("firstname")
        self.last_name: str = kwargs.get("lastname")
        self.former_first_name: str = kwargs.get("formerfirstname")
        self.former_last_name: str = kwargs.get("formerlastname")
        self.avatar: str = kwargs.get("avatar")
        self.banner: str = kwargs.get("banner")
        self.twitter: str = kwargs.get("twitter")
        self.youtube: str = kwargs.get("youtube")
        self.melon: str = kwargs.get("melon")
        self.instagram: str = kwargs.get("instagram")
        self.vlive: str = kwargs.get("vlive")
        self.spotify: str = kwargs.get("spotify")
        self.fancafe: str = kwargs.get("fancafe")
        self.facebook: str = kwargs.get("facebook")
        self.tiktok: str = kwargs.get("tiktok")
        self.city: str = kwargs.get("city")
        self.country: str = kwargs.get("country")
        self.blood_type: str = kwargs.get("bloodtype")
        self.gender: str = kwargs.get("gender")
        self.description: str = kwargs.get("description")
        self.height: int = kwargs.get("height")
        self.call_count: int = kwargs.get("callcount")
        self.tags = kwargs.get("tags")
        _persons[self.id] = self
        ...

    @staticmethod
    async def create(*args, **kwargs):
        """Create a Person object."""
        person_id = kwargs.get("personid")
        date = await Date.get(kwargs.get("dateid"))
        name = await Name.get(kwargs.get("nameid"))
        # TODO: Create

        former_name = await Name.get(kwargs.get("formernameid"))


        return Person(*args)

    @staticmethod
    async def get(person_id: int):
        """Get a Person object.

        If the Person object does not exist in cache, it will fetch the person from the API.
        :param person_id: (int) The ID of the person to get/fetch.
        """
        existing_person = _persons.get(person_id)
        if not existing_person:
            return await Person.fetch(person_id)

    @staticmethod
    async def fetch(person_id: int):
        """Fetch an updated Person object from the API.

        # NOTE: Person objects are added to cache on creation.

        :param person_id: (int) The person's ID to fetch.
        """
        return internal_fetch(obj=Person, request={
            'route': 'person/$person_id',
            'person_id': person_id,
            'method': 'GET'}
        )

    @staticmethod
    async def fetch_all_persons():
        """Fetch all persons.

        # NOTE: Person objects are added to cache on creation.
        """
        return internal_fetch_all(obj=Person, request={
            'route': 'person/',
            'method': 'GET'}
        )


_persons: Dict[int, Person] = dict()

