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
    Difficulty,
    get_difficulty,
    basic_call,
    Subscription,
    Channel
)


class TwitchAccount(Subscription):
    r"""Represents a Twitch Account.

    A TwitchAccount object inherits from :ref:`Subscription`.

    Parameters
    ----------
    username: str
        The twitch account username
    channels_following: Optional[List[:ref:`Channel`]]
        The channels following the Twitch account
    mention_roles: Optional[Dict[Channel, int]]
        The role ids of channels that need mentioning on updates.
    """

    def __init__(self, username: str,
                 channels_following: Optional[List[Channel]] = None,
                 mention_roles: Optional[Dict[Channel, int]] = None):
        super(TwitchAccount, self).__init__(account_id=username,
                                            account_name=username,
                                            followed=channels_following)

        if not _accounts.get(self.id):
            # we need to make sure not to override the current object in cache.
            _accounts[self.id] = self
        else:
            account = _accounts[self.id] = self
            for channel in channels_following:
                account._sub_in_cache(channel, role_id=mention_roles.get(channel.id))

    @staticmethod
    async def create(*args, **kwargs):
        """
        Create a TwitchAccount object.

        :returns: :ref:`TwitchAccount`
        """
        # if a bundle of accounts is sent in, create them all.
        if not kwargs.get("username"):
            if len(kwargs.keys()) == 1:
                return await TwitchAccount.create(**kwargs["0"])

            for key in kwargs.keys():
                await TwitchAccount.create(**kwargs[key])

        username = kwargs.get("username")
        channel_id = kwargs.get("channelid")
        channel = await Channel.get(channel_id)
        if not channel:
            await Channel.insert(channel_id)
            channel = await Channel.get(channel_id)

        if not channel.guild_id:
            channel.guild_id = kwargs.get("guildid")

        role_id = kwargs.get("roleid")

        TwitchAccount(username, [channel], dict({channel: role_id}))

        return _accounts[username]

    async def update_posted(self, channel_ids: List[int], posted: bool) -> None:
        """
        Update the media and status ids for the game in the database.

        :param channel_ids: List[int]
            All channel IDs that need the posted attribute changed.
        :param posted: bool
            Whether the update has been posted to the channels.
        :return: None
        """
        await basic_call(request={
            "route": "twitch/$username",
            "username": self.name,
            "channel_ids": channel_ids,
            "posted": posted,
            "method": "PUT"
        })

    async def unsubscribe(self, channel: Union[Channel]):
        # if channel not in self:
        #     return

        await basic_call(request={
            "route": "twitch/$username",
            "username": self.name,
            "channel_id": channel.id,
            "method": "DELETE"
        })
        self._unsub_in_cache(channel)

    async def subscribe(self, channel: Channel, role_id: Optional[int] = None):
        if channel in self:
            return

        await basic_call(request={
            "route": "twitch/$username",
            "username": self.name,
            "channel_id": channel.id,
            "guild_id": channel.guild_id,
            "role_id": role_id,
            "method": "POST"
        })
        self._sub_in_cache(channel, role_id)

    async def _remove_from_cache(self) -> None:
        """
        Remove the TwitchAccount object from cache.

        :returns: None
        """
        _accounts.pop(self.id)

    @staticmethod
    async def insert(username: str, guild_id: int, channel_id: int, role_id: Optional[int]):
        """
        Insert a new TwitchAccount into the database.

        :param username: int
            The Twitch Account username.
        :param guild_id: int
            The first guild ID that is subscribing.
        :param channel_id: int
            The first channel id that is subscribing.
        :param role_id: Optional[int]
            A role to notify.

        :return: :ref:`TwitchAccount`
            The TwitchAccount object.
        """
        await basic_call(request={
            "route": "twitch/$username",
            "username": username,
            "channel_id": channel_id,
            "guild_id": guild_id,
            "role_id": role_id,
            "method": "POST"
        })

        # have the model created and added to cache.
        twitch_account = await TwitchAccount.fetch(username)
        return twitch_account

    @staticmethod
    async def get(username: str, fetch=True):
        """Get a TwitchAccount object.

        If the TwitchAccount object does not exist in cache, it will fetch the id from the API.
        :param username: str
            The twitch account username.
        :param fetch: bool
            Whether to fetch from the API if not found in cache.
        :returns: Optional[:ref:`TwitchAccount`]
            The TwitchAccount object requested.
        """
        username = username.lower()
        existing = _accounts.get(username)
        if not existing and fetch:
            return await TwitchAccount.fetch(username)
        return existing

    @staticmethod
    async def get_all():
        """
        Get all TwitchAccount objects in cache.

        :returns: dict_values[:ref:`TwitchAccount`]
            All TwitchAccount objects from cache.
        """
        return _accounts.values()

    @staticmethod
    async def fetch(username: str):
        """Fetch an updated TwitchAccount object from the API.

        .. NOTE:: affiliation objects are added to cache on creation.

        :param username: int
            The Twitch account username to fetch.
        :returns: Optional[:ref:`TwitchAccount`]
            The TwitchAccount object requested.
        """
        return await internal_fetch(
            obj=TwitchAccount,
            request={
                "route": "twitch/$username",
                "username": username,
                "method": "GET",
            },
        )

    @staticmethod
    async def fetch_all():
        """Fetch all TwitchAccount objects.

        .. NOTE:: TwitchAccount objects are added to cache on creation.
        """
        return await internal_fetch_all(
            obj=TwitchAccount, request={"route": "twitch", "method": "GET"}
        )


_accounts: Dict[str, TwitchAccount] = dict()
