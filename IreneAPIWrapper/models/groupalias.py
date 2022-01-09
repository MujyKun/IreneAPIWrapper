from typing import Union, List, Optional, Dict

from IreneAPIWrapper.sections import outer
from . import CallBack, Access, AbstractModel, internal_fetch, internal_fetch_all, MediaSource, Alias


class GroupAlias(Alias, AbstractModel):
    def __init__(self, alias_id, alias_name, group_id, guild_id):
        super(GroupAlias, self).__init__(alias_id=alias_id, alias_name=alias_name, obj_id=group_id, guild_id=guild_id)
        _groupaliases[self.id] = self

    @staticmethod
    async def create(*args, **kwargs):
        alias_id = kwargs.get("aliasid")
        name = kwargs.get("alias")
        group_id = kwargs.get("groupid")
        guild_id = kwargs.get("guildid")
        return GroupAlias(alias_id, name, group_id, guild_id)

    @staticmethod
    async def get(group_alias_id: int, fetch=True):
        """Get a GroupAlias object.

        If the GroupAlias object does not exist in cache, it will fetch the name from the API.
        :param group_alias_id: (int) The ID of the name to get/fetch.
        :param fetch: (bool) Whether to fetch from the API if not found in cache.
        """
        existing = _groupaliases.get(group_alias_id)
        if not existing and fetch:
            return await GroupAlias.fetch(group_alias_id)
        return existing

    @staticmethod
    async def fetch(group_alias_id: int):
        """Fetch an updated GroupAlias object from the API.

        # NOTE: GroupAlias objects are added to cache on creation.

        :param group_alias_id: (int) The group alias's ID to fetch.
        """
        return await internal_fetch(obj=GroupAlias, request={
            'route': 'groupalias/$alias_id',
            'alias_id': group_alias_id,
            'method': 'GET'}
        )

    @staticmethod
    async def fetch_all():
        """Fetch all group aliases.

        # NOTE: GroupAlias objects are added to cache on creation.
        """
        return await internal_fetch_all(obj=GroupAlias, request={
            'route': 'groupalias/',
            'method': 'GET'}
        )


_groupaliases: Dict[int, GroupAlias] = dict()
