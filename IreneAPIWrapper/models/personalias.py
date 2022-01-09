from typing import Union, List, Optional, Dict

from IreneAPIWrapper.sections import outer
from . import CallBack, Access, AbstractModel, internal_fetch, internal_fetch_all, MediaSource, Alias


class PersonAlias(AbstractModel, Alias):
    def __init__(self, alias_id, alias_name, person_id, guild_id):
        super(PersonAlias, self).__init__(alias_id=alias_id, alias_name=alias_name, obj_id=person_id, guild_id=guild_id)
        _personaliases[self.id] = self

    async def create(self, *args, **kwargs):
        alias_id = kwargs.get("aliasid")
        name = kwargs.get("alias")
        person_id = kwargs.get("personid")
        guild_id = kwargs.get("guildid")
        return PersonAlias(alias_id, name, person_id, guild_id)

    @staticmethod
    async def get(person_alias_id: int):
        """Get a PersonAlias object.

        If the PersonAlias object does not exist in cache, it will fetch the name from the API.
        :param person_alias_id: (int) The ID of the name to get/fetch.
        """
        existing_person = _personaliases.get(person_alias_id)
        if not existing_person:
            return await PersonAlias.fetch(person_alias_id)

    @staticmethod
    async def fetch(person_alias_id: int):
        """Fetch an updated PersonAlias object from the API.

        # NOTE: PersonAlias objects are added to cache on creation.

        :param person_alias_id: (int) The person alias's ID to fetch.
        """
        return internal_fetch(obj=PersonAlias, request={
            'route': 'personalias/$person_alias_id',
            'person_alias_id': person_alias_id,
            'method': 'GET'}
        )

    @staticmethod
    async def fetch_all():
        """Fetch all person aliases.

        # NOTE: PersonAlias objects are added to cache on creation.
        """
        return internal_fetch_all(obj=PersonAlias, request={
            'route': 'personalias/',
            'method': 'GET'}
        )


_personaliases: Dict[int, PersonAlias] = dict()
