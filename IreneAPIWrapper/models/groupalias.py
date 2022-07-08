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


class GroupAlias(Alias):
    r"""Represents the alias of a :ref:`Group`.

    A GroupAlias object inherits from :ref:`Alias` which inherits from :ref:`AbstractModel`.

    Parameters
    ----------
    alias_id: int
        The Alias id.
    alias_name: str
        The alias name.
    group_id: int
        The ID of the :ref:`Group` the alias is referring to.
    guild_id: Optional[int]
        A guild ID that owns the alias if there is one.

    Attributes
    ----------
    id: int
        The Alias id.
    name: str
        The alias name.
    _obj_id: int
        The :ref:`Group` ID the alias is referring to. Used for Abstraction.
    group_id: int
        The :ref:`Group` ID the alias is referring to.
    guild_id: Optional[int]
         A guild ID that owns the alias if there is one.
    """

    def __init__(self, alias_id, alias_name, group_id, guild_id):
        super(GroupAlias, self).__init__(
            alias_id=alias_id, alias_name=alias_name, obj_id=group_id, guild_id=guild_id
        )
        self.group_id = group_id
        if not _groupaliases.get(self.id):
            _groupaliases[self.id] = self

    @staticmethod
    async def create(*args, **kwargs):
        """
        Create a GroupAlias object.

        :return: :ref:`GroupAlias`
        """
        alias_id = kwargs.get("aliasid")
        name = kwargs.get("alias")
        group_id = kwargs.get("groupid")
        guild_id = kwargs.get("guildid")
        GroupAlias(alias_id, name, group_id, guild_id)
        return _groupaliases[alias_id]

    async def delete(self) -> None:
        """
        Delete the GroupAlias object from the database and remove it from cache.

        :returns: None
        """
        await internal_delete(
            self,
            request={
                "route": "groupalias/$alias_id",
                "alias_id": self.id,
                "method": "DELETE",
            },
        )
        await self._remove_from_cache()

    async def _remove_from_cache(self) -> None:
        """
        Remove the GroupAlias object from cache.

        :returns: None
        """
        _groupaliases.pop(self.id)

    @staticmethod
    async def insert(group_id: int, alias: str, guild_id: int = None) -> bool:
        """
        Insert a new GroupAlias into the database.

        :param group_id: int
            The :ref:`Group`'s ID.
        :param alias: str
            The alias of the :ref:`Group` to add.
        :param guild_id: Optional[int]
            A guild that owns this alias.
        :return: bool
            Whether the GroupAlias was added to the existing objects as well as inserted into the DB.
        """
        request = {
            "route": "groupalias",
            "alias": alias,
            "group_id": group_id,
            "method": "POST",
        }
        if guild_id:
            request["guild_id"] = guild_id

        callback = await internal_insert(request=request)
        results = callback.response.get("results")

        if not results:
            return False

        # TODO: Confirm the correct return is t_alias_id
        group_alias = await GroupAlias.fetch(results.get("t_alias_id"))

        from . import Group

        group = await Group.get(group_id, fetch=False)
        if group:
            group.aliases.append(group_alias)
        return True

    @staticmethod
    async def get(group_alias_id: int, fetch=True):
        """Get a GroupAlias object.

        If the GroupAlias object does not exist in cache, it will fetch the name from the API.
        :param group_alias_id: int
            The ID of the group alias to get/fetch.
        :param fetch: bool
            Whether to fetch from the API if not found in cache.
        :returns: :ref:`GroupAlias`
        """
        existing = _groupaliases.get(group_alias_id)
        if not existing and fetch:
            return await GroupAlias.fetch(group_alias_id)
        return existing

    @staticmethod
    async def get_all():
        """
        Get all GroupAlias objects in cache.

        :returns: dict_values[:ref:`GroupAlias`]
            All GroupAlias objects from cache.
        """
        return _groupaliases.values()

    @staticmethod
    async def fetch(group_alias_id: int):
        """Fetch an updated GroupAlias object from the API.

        .. NOTE::: GroupAlias objects are added to cache on creation.

        :param group_alias_id: int
            The group alias's ID to fetch.
        :returns: :ref:`GroupAlias`
        """
        return await internal_fetch(
            obj=GroupAlias,
            request={
                "route": "groupalias/$alias_id",
                "alias_id": group_alias_id,
                "method": "GET",
            },
        )

    @staticmethod
    async def fetch_all():
        """Fetch all group aliases.

        .. NOTE::: GroupAlias objects are added to cache on creation.
        """
        return await internal_fetch_all(
            obj=GroupAlias, request={"route": "groupalias/", "method": "GET"}
        )


_groupaliases: Dict[int, GroupAlias] = dict()
