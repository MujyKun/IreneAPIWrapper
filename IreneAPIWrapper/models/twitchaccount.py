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
                                            followed=channels_following,
                                            mention_roles=mention_roles)
        self._update_channels = False
        acc = _accounts.get(self.id)
        if not acc:
            # we need to make sure not to override the current object in cache.
            _accounts[self.id] = self
        else:
            acc._sub_in_cache(channels=channels_following, role_ids=mention_roles)

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

    @staticmethod
    async def create_bulk(list_of_dicts: List[dict]):
        """Bulk create TwitchAccount objects.

        :param list_of_dicts: List[dict]
            A list of dictionaries.
        :returns: Optional[List[:ref:`TwitchAccount`]]
        """
        final_channels = {}
        final_roles = {}
        for _dictionary in list_of_dicts:
            username = _dictionary["username"]
            guild_id = _dictionary["guildid"]
            channel_id = _dictionary["channelid"]
            # posted = _dictionary["posted"]
            role_id = _dictionary["roleid"]

            channel = await Channel.get(channel_id)
            if not channel:
                await channel.insert(channel_id)
                channel = await Channel.get(channel_id)

            if not channel.guild_id:
                channel.guild_id = guild_id

            if not final_channels.get(username):
                final_channels[username] = [channel]
            else:
                final_channels[username].append(channel)

            if role_id:
                if not final_roles.get(username):
                    final_roles[username] = dict({Channel: role_id})
                else:
                    final_roles[username][Channel] = role_id

        final_twitch_channels = []
        for _user, _channels in final_channels.items():
            TwitchAccount(_user, _channels, final_roles.get(_user))
            obj = await TwitchAccount.get(_user, fetch=False)
            final_twitch_channels.append(obj)

        return final_twitch_channels

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

    async def is_live(self) -> bool:
        """
        Check if the current twitch account is live.

        :return: bool
        """
        dict_response = await self.is_live_bulk([self])
        return dict_response[self.id]

    @staticmethod
    async def is_live_bulk(accounts: List[AbstractModel]) -> Dict[AbstractModel, bool]:
        """
        A list of Twitch accounts.

        :param accounts: List[:ref:`TwitchAccount`]
            A list of twitch accounts.
        :returns: Dict[:ref:`TwitchAccount`, bool]
            A dictionary with the key as the account and the value if they are live.
        """
        callback = await basic_call(request={
            "route": "twitch/is_live/$username",
            "usernames": [account.id for account in accounts],
            "method": "GET"
        })

        return {}

    def check_subscribed(self, channels: List[Channel]) -> List[Channel]:
        """Checks which :ref:`Channel`s are subscribed to the current twitch account
        from a selection of channels.

        :param channels: List[:ref:`Channel`]
        :returns List[:ref:`Channel`]
            A list of :ref:`Channel`s from the channels provided that are subscribed.
        """
        return [channel for channel in channels if channel in self]


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
    async def subbed_in(guild_id):
        """
        Get the twitch channels subscribed to in a Guild.

        :param guild_id: The guild ID.
        :return: Optional[List[:ref:`TwitchAccount`]]
        """
        return await internal_fetch_all(TwitchAccount, request={
            'route': 'twitch/filter/$guild_id',
            'guild_id': guild_id,
            'method': 'GET'
        })

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
            obj=TwitchAccount, request={"route": "twitch", "method": "GET"},
            bulk=True)


_accounts: Dict[str, TwitchAccount] = dict()
