from typing import Union, List, Optional, Dict

from IreneAPIWrapper.sections import outer
from . import (
    CallBack,
    Access,
    AbstractModel,
    internal_fetch,
    internal_fetch_all,
    MediaSource,
    Alias,
    internal_delete,
    internal_insert,
)


class PersonAlias(Alias):
    r"""Represents the alias of a :ref:`Person`.

    A PersonAlias object inherits from :ref:`Alias` which inherits from :ref:`AbstractModel`.

    Parameters
    ----------
    alias_id: int
        The Alias id.
    alias_name: str
        The alias name.
    person_id: int
        The ID of the :ref:`Person` the alias is referring to.
    guild_id: Optional[int]
        A guild ID that owns the alias if there is one.

    Attributes
    ----------
    id: int
        The Alias id.
    name: str
        The alias name.
    _obj_id: int
        The :ref:`Person` ID the alias is referring to. Used for Abstraction.
    person_id: int
        The :ref:`Person` ID the alias is referring to.
    guild_id: Optional[int]
         A guild ID that owns the alias if there is one.
    """

    def __init__(self, alias_id, alias_name, person_id, guild_id):
        super(PersonAlias, self).__init__(
            alias_id=alias_id,
            alias_name=alias_name,
            obj_id=person_id,
            guild_id=guild_id,
        )
        self.person_id = person_id
        if not _personaliases.get(self.id):
            _personaliases[self.id] = self

    @staticmethod
    async def create(*args, **kwargs):
        """
        Create a PersonAlias object.

        :returns: :ref:`PersonAlias`
        """
        alias_id = kwargs.get("aliasid")
        name = kwargs.get("alias")
        person_id = kwargs.get("personid")
        guild_id = kwargs.get("guildid")
        PersonAlias(alias_id, name, person_id, guild_id)
        return _personaliases[alias_id]

    async def delete(self) -> None:
        """
        Delete the PersonAlias object from the database and remove it from cache.

        :returns: None
        """
        await internal_delete(
            self,
            request={
                "route": "personalias/$alias_id",
                "alias_id": self.id,
                "method": "DELETE",
            },
        )
        await self._remove_from_cache()

    async def _remove_from_cache(self) -> None:
        """
        Remove the PersonAlias object from cache.

        :returns: None
        """
        _personaliases.pop(self.id)

    @staticmethod
    async def insert(person_id: int, alias: str, guild_id: int = None) -> bool:
        """
        Insert a new PersonAlias into the database.

        :param person_id: int
            The :ref:`Group`'s ID.
        :param alias: str
            The alias of the :ref:`Person` to add.
        :param guild_id: Optional[int]
            A guild that owns this alias.
        :return: bool
            Whether the PersonAlias was added to the existing objects as well as inserted into the DB.
        """
        request = {
            "route": "personalias",
            "alias": alias,
            "person_id": person_id,
            "method": "POST",
        }
        if guild_id:
            request["guild_id"] = guild_id

        callback = await internal_insert(request=request)
        results = callback.response.get("results")

        if not results:
            return False

        # TODO: Confirm the correct return is t_alias_id
        person_alias = await PersonAlias.fetch(results.get("t_alias_id"))
        if not person_alias:
            return False

        from . import Person

        person = await Person.get(person_id, fetch=False)
        if person:
            person.aliases.append(person_alias)
        return True

    @staticmethod
    async def get(person_alias_id: int, fetch=True):
        """Get a PersonAlias object.

        If the PersonAlias object does not exist in cache, it will fetch the name from the API.
        :param person_alias_id: int
            The ID of the name to get/fetch.
        :param fetch: bool
            Whether to fetch from the API if not found in cache.
        :returns: :ref:`PersonAlias`
        """
        existing = _personaliases.get(person_alias_id)
        if not existing and fetch:
            return await PersonAlias.fetch(person_alias_id)
        return existing

    @staticmethod
    async def get_all():
        """
        Get all PersonAlias objects in cache.

        :returns: dict_values[:ref:`PersonAlias`]
            All PersonAlias objects from cache.
        """
        return _personaliases.values()

    @staticmethod
    async def fetch(person_alias_id: int):
        """Fetch an updated PersonAlias object from the API.

        .. NOTE::: PersonAlias objects are added to cache on creation.

        :param person_alias_id: int
            The person alias's ID to fetch.
        :returns: :ref:`PersonAlias`

        """
        return await internal_fetch(
            obj=PersonAlias,
            request={
                "route": "personalias/$alias_id",
                "alias_id": person_alias_id,
                "method": "GET",
            },
        )

    @staticmethod
    async def fetch_all():
        """Fetch all person aliases.

        .. NOTE::: PersonAlias objects are added to cache on creation.
        """
        return await internal_fetch_all(
            obj=PersonAlias, request={"route": "personalias/", "method": "GET"}
        )


_personaliases: Dict[int, PersonAlias] = dict()
