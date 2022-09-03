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


class Channel(AbstractModel):
    r"""Represents a discord channel.

    A Channel object inherits from :ref:`AbstractModel`.

    Parameters
    ----------
    channel_id: int
        The channel id.

    Attributes
    ----------
    id: int
        The channel id.
    guild_id: Optional[int]
        The guild ID.
    """

    def __init__(self, channel_id, guild_id=None):
        super(Channel, self).__init__(channel_id)

        self.guild_id: Optional[int] = guild_id

        if not _channels.get(self.id):
            _channels[self.id] = self

    @staticmethod
    async def create(*args, **kwargs):
        """
        Create a Channel object.

        :returns: :ref:`Channel`
        """
        channel_id = kwargs.get("channelid")
        guild_id = kwargs.get("guildid")
        Channel(channel_id, guild_id)
        return _channels[channel_id]

    async def delete(self) -> None:
        """
        Delete a Channel object from the database and remove it from cache.

        .. Warning:: This will cascade all objects dependent on the object.

        :return: None
        """
        await internal_delete(
            self,
            request={
                "route": "channel/$channel_id",
                "channel_id": self.id,
                "method": "DELETE",
            },
        )

    async def _remove_from_cache(self) -> None:
        """
        Remove the Channel object from cache.

        :return: None
        """
        _channels.pop(self.id)

    @staticmethod
    async def insert(channel_id, guild_id) -> None:
        """
        Insert a new channel into the database.

        :param channel_id: The channel ID to insert.
        :param guild_id: The guild ID to insert.
        :return: None
        """
        await internal_insert(
            request={
                "route": "channel",
                "channel_id": channel_id,
                "guild_id": guild_id,
                "method": "POST",
            }
        )

    @staticmethod
    async def get(channel_id: int, fetch=True):
        r"""
        Get a Channel object.

        If the Channel object does not exist in cache, it will fetch the name from the API.

        :param channel_id: int
            The channel ID to retrieve.
        :param fetch: bool
            Whether to fetch from the API if not found in cache.
        :returns: Optional[:ref:`Channel`]
            The channel object requested.
        """
        existing = _channels.get(channel_id)
        if not existing and fetch:
            return await Channel.fetch(channel_id)
        return existing

    @staticmethod
    async def get_all():
        """
        Get all Channel objects in cache.

        :returns: dict_values[:ref:`Channel`]
            All Channel objects from cache.
        """
        return _channels.values()

    @staticmethod
    async def fetch(channel_id):
        """
        Fetch an updated channel object from the API.

        .. NOTE::: channel objects are added to cache on creation.

        :param channel_id: int
            The channel ID to fetch.
        :returns: Optional[:ref:`Channel`]
            The channel object requested.
        """
        return await internal_fetch(
            obj=Channel,
            request={
                "route": "channel/$channel_id",
                "channel_id": channel_id,
                "method": "GET",
            },
        )

    @staticmethod
    async def fetch_all():
        """Fetch all Channels.

        .. NOTE:: Channel objects are added to cache on creation.
        """
        return await internal_fetch_all(
            obj=Channel, request={"route": "channel", "method": "GET"}
        )


_channels: Dict[int, Channel] = dict()
