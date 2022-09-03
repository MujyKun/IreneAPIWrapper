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
    Channel,
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

    def __init__(
        self,
        username: str,
        channels_following: Optional[List[Channel]] = None,
        mention_roles: Optional[Dict[Channel, int]] = None,
    ):
        super(TwitchAccount, self).__init__(
            account_id=username,
            account_name=username,
            followed=channels_following,
            mention_roles=mention_roles,
        )
        acc = _accounts.get(self.id)
        self.is_live = False
        if not acc:
            # we need to make sure not to override the current object in cache.
            _accounts[self.id] = self
        else:
            acc._sub_in_cache(channels=channels_following, role_ids=mention_roles)

    @staticmethod
    async def create(*args, **kwargs):
        """
        Create a TwitchAccount object.

        If several rows containing the same accounts are being passed in,
        use :ref:`create_bulk` instead for proper optimization.
        This will happen by default in a fallback if multiple rows are detected.

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
        if not channel:  # should never be the case.
            await Channel.insert(channel_id, None)
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
            guild_id = _dictionary.get("guildid")
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
                    final_roles[username] = dict({channel: role_id})
                else:
                    final_roles[username][channel] = role_id

        final_twitch_channels = []
        for _user, _channels in final_channels.items():
            TwitchAccount(_user, _channels, final_roles.get(_user))
            obj = await TwitchAccount.get(_user, fetch=False)
            final_twitch_channels.append(obj)

        return final_twitch_channels

    async def get_posted(self) -> List[Channel]:
        """
        Get a list of channels that have already posted to discord.
        :return: List[:ref:`Channel`]
        """
        callback = await basic_call(
            request={
                "route": "twitch/already_posted/$username",
                "username": self.id,
                "method": "GET",
            }
        )
        results = callback.response.get("results")
        if not results:
            return []

        channel_ids = [row["channelid"] for row in results.values()]
        channels = [await Channel.get(channel_id) for channel_id in channel_ids]
        return channels

    async def update_posted(self, channel_ids: List[int], posted: bool) -> None:
        """
        Update the media and status ids for the game in the database.

        :param channel_ids: List[int]
            All channel IDs that need the posted attribute changed.
        :param posted: bool
            Whether the update has been posted to the channels.
        :return: None
        """
        if not channel_ids:
            return

        await basic_call(
            request={
                "route": "twitch/$username",
                "username": self.name,
                "channel_ids": channel_ids,
                "posted": posted,
                "method": "PUT",
            }
        )

    async def check_live(self) -> bool:
        """
        Check if the current twitch account is live.

        :return: bool
        """
        dict_response = await self.check_live_bulk([self])
        return dict_response[self.id]

    @staticmethod
    async def check_live_bulk(accounts: List[AbstractModel]) -> Dict[str, bool]:
        """
        A list of Twitch accounts.

        :param accounts: List[:ref:`TwitchAccount`]
            A list of twitch accounts.
        :returns: Dict[:ref:`str`, bool]
            A dictionary with the key as the username and the value if they are live.
        """
        callback = await basic_call(
            request={
                "route": "twitch/is_live",
                "usernames": [account.id for account in accounts],
                "method": "GET",
            }
        )

        live_dict: Dict[str, bool] = callback.response["results"]
        for user, is_live in live_dict.items():
            acc = await TwitchAccount.get(user)
            acc.is_live = is_live
        return live_dict

    @staticmethod
    async def check_user_exists(username) -> bool:
        """
        Check if a twitch username exists.

        :param username: The twitch display or login username.
        :return: bool
            Whether the username exists.
        """
        callback = await basic_call(
            request={
                "route": "twitch/exists/$username",
                "username": username.lower(),
                "method": "GET",
            }
        )
        return callback.response["results"]

    async def unsubscribe(self, channel: Union[Channel]):
        """
        Have a channel unsubscribe from the account if it is not already.


        :param channel: :ref:`Channel`
            The channel to unsubscribe from the account.
        """
        if channel not in self:
            return

        await basic_call(
            request={
                "route": "twitch/$username",
                "username": self.name,
                "channel_id": channel.id,
                "method": "DELETE",
            }
        )
        self._unsub_in_cache(channel)

    async def subscribe(self, channel: Channel, role_id: Optional[int] = None):
        if channel in self:
            # check for a role id update
            if await self.get_role_id(channel) != role_id:
                # unsubscribe them, then we resubscribe with the new role id.
                await self.unsubscribe(channel)
            return

        await basic_call(
            request={
                "route": "twitch/$username",
                "username": self.name,
                "channel_id": channel.id,
                "role_id": role_id,
                "method": "POST",
            }
        )
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
        return await internal_fetch_all(
            TwitchAccount,
            request={
                "route": "twitch/filter/$guild_id",
                "guild_id": guild_id,
                "method": "GET",
            },
        )

    @staticmethod
    async def insert(username: str, channel_id: int, role_id: Optional[int]):
        """
        Insert a new TwitchAccount into the database.

        :param username: int
            The Twitch Account username.
        :param channel_id: int
            The first channel id that is subscribing.
        :param role_id: Optional[int]
            A role to notify.

        :return: :ref:`TwitchAccount`
            The TwitchAccount object.
        """
        await basic_call(
            request={
                "route": "twitch/$username",
                "username": username,
                "channel_id": channel_id,
                "role_id": role_id,
                "method": "POST",
            }
        )

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
            obj=TwitchAccount, request={"route": "twitch", "method": "GET"}, bulk=True
        )


_accounts: Dict[str, TwitchAccount] = dict()
