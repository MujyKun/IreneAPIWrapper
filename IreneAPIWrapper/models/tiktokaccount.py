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


class TikTokAccount(Subscription):
    r"""Represents a TikTok Account.

    A TikTokAccount object inherits from :ref:`Subscription`.

    Parameters
    ----------
    username: str
        The TikTok account username
    user_ids: List[int]
        The users (id) who requested the subscription to this user.
    channels_following: Optional[List[:ref:`Channel`]]
        The channels following the TikTok account
    mention_roles: Optional[Dict[Channel, int]]
        The role ids of channels that need mentioning on updates.
    """

    def __init__(
        self,
        username: str,
        user_ids: List[int] = None,
        channels_following: Optional[List[Channel]] = None,
        mention_roles: Optional[Dict[Channel, int]] = None,
    ):
        super(TikTokAccount, self).__init__(
            account_id=username,
            account_name=username,
            followed=channels_following,
            mention_roles=mention_roles,
        )

        self.user_ids = user_ids or []

        acc = _accounts.get(self.id)
        if not acc:
            # we need to make sure not to override the current object in cache.
            _accounts[self.id] = self
        else:
            acc._sub_in_cache(channels=channels_following, role_ids=mention_roles)

    @staticmethod
    async def create(*args, **kwargs):
        """
        Create a TikTokAccount object.

        If several rows containing the same accounts are being passed in,
        use :ref:`create_bulk` instead for proper optimization.
        This will happen by default in a fallback if multiple rows are detected.

        :returns: :ref:`TikTokAccount`
        """
        # if a bundle of accounts is sent in, create them all.
        if not kwargs.get("username"):
            if len(kwargs.keys()) == 1:
                return await TikTokAccount.create(**kwargs["0"])

            for key in kwargs.keys():
                await TikTokAccount.create(**kwargs[key])

        username = kwargs.get("username")
        user_id = kwargs.get("userid")
        channel_id = kwargs.get("channelid")
        channel = await Channel.get(channel_id)
        if not channel:  # should never be the case.
            await Channel.insert(channel_id, None)
            channel = await Channel.get(channel_id)

        setattr(channel, "user_id", user_id)

        if not channel.guild_id:
            channel.guild_id = kwargs.get("guildid")

        role_id = kwargs.get("roleid")

        TikTokAccount(username, [user_id], [channel], dict({channel: role_id}))
        return _accounts[username]

    async def get_latest_video_id(self) -> Optional[int]:
        """
        Get the latest TikTok video ID of the account.

        :return: int
            The latest video ID.
            Will return -1 if the user could not be found.
        """
        callback = await basic_call(
            request={
                "route": "tiktok/latest_video/$username",
                "username": self.name,
                "method": "GET",
            }
        )
        # results = callback.response["results"]
        if callback.response.get("status", "") == "User does not exist.":
            return -1

        result = callback.response.get(self.name)
        return int(result) if result is not None else result

    @staticmethod
    async def create_bulk(list_of_dicts: List[dict]):
        """Bulk create TikTokAccount objects.

        :param list_of_dicts: List[dict]
            A list of dictionaries.
        :returns: Optional[List[:ref:`TikTokAccount`]]
        """
        final_channels = {}
        final_roles = {}
        final_user_ids = {}
        for _dictionary in list_of_dicts:
            username = _dictionary["username"]
            user_id = _dictionary["userid"]
            guild_id = _dictionary.get("guildid")
            channel_id = _dictionary["channelid"]
            # posted = _dictionary["posted"]
            role_id = _dictionary["roleid"]

            final_user_ids[username] = final_user_ids.get(username, []) + [user_id]

            channel = await Channel.get(channel_id)
            if not channel:
                await channel.insert(channel_id)
                channel = await Channel.get(channel_id)
            setattr(channel, "user_id", user_id)

            if not channel.guild_id:
                channel.guild_id = guild_id

            final_channels[username] = final_channels.get(username, []) + [channel]

            if role_id:
                # sets the default username to contain an empty dict of the channel, and then assign it a role id.
                (final_roles.setdefault(username, {}))[channel] = role_id

        final_tiktok_channels = []
        for _user, _channels in final_channels.items():
            TikTokAccount(_user, final_user_ids.get(_user), _channels, final_roles.get(_user))
            obj = await TikTokAccount.get(_user, fetch=False)
            final_tiktok_channels.append(obj)

        return final_tiktok_channels

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
                "route": "tiktok/$username",
                "username": self.name,
                "channel_id": channel.id,
                "method": "DELETE",
            }
        )
        self._unsub_in_cache(channel)

    def _unsub_in_cache(self, channel: Channel):
        """
        Make a channel unsubscribe.

        :param channel: :ref:`Channel`
            A :ref:`Channel` object to remove from cache.
        """
        if channel in self._followed:
            self._followed.remove(channel)

        if self._mention_roles.get(channel):
            self._mention_roles.pop(channel)

        user_id = getattr(channel, "user_id", None)
        if user_id:
            self.user_ids.remove(user_id)

    async def subscribe(self, channel: Channel, role_id: Optional[int] = None, user_id=None):
        if channel in self:
            # check for a role id update
            if await self.get_role_id(channel) != role_id:
                # unsubscribe them, then we resubscribe with the new role id.
                await self.unsubscribe(channel)
            return

        if not user_id:
            # a user_id is actually required here, but we don't want to alter the method signature
            raise NotImplementedError

        setattr(channel, "user_id", user_id)

        if await self.insert(self.id, user_id, channel.id, role_id, fetch=False) is False:
            return False
        self._sub_in_cache(channel, user_id, role_id)

    def _sub_in_cache(
        self,
        channel: Channel = None,
        user_id: int = None,
        role_id: int = None,
        channels: Optional[List[Channel]] = None,
        role_ids: Optional[Dict[Channel, int]] = None,
    ):
        """
        Make a channel subscribe.

        :param channel: Union[:ref:`Channel`, List[:ref:`Channel`]
            A :ref:`Channel` object to add to cache.
        :param role_id: int
            The role ID to add.
        """
        if channel and channel not in self:
            self._followed.append(channel)

        if role_id and channel:
            self._mention_roles[channel] = role_id

        if channels:
            self._followed += [
                _channel for _channel in channels if _channel not in self._followed
            ]

        if role_ids:
            self._mention_roles |= role_ids  # merge the dictionaries.

        if user_id:
            if user_id not in self.user_ids:
                self.user_ids.append(user_id)

    async def _remove_from_cache(self) -> None:
        """
        Remove the TikTokAccount object from cache.

        :returns: None
        """
        _accounts.pop(self.id)

    @staticmethod
    async def insert(username: str, user_id: int, channel_id: int, role_id: Optional[int], fetch=True):
        """
        Insert a new TikTokAccount into the database.

        :param username: int
            The TikTok Account username.
        :param user_id: int
            The user who requested the insert.
        :param channel_id: int
            The first channel id that is subscribing.
        :param role_id: Optional[int]
            A role to notify.
        :param fetch: bool
            Whether to fetch the object.


        :return: :ref:`TikTokAccount`
            The TikTokAccount object.
        """
        callback = await basic_call(
            request={
                "route": "tiktok",
                "username": username,
                "user_id": user_id,
                "channel_id": channel_id,
                "role_id": role_id,
                "method": "POST",
            }
        )

        if 'User does not exist.' in callback.response.get('status', ''):
            return False

        # have the model created and added to cache.
        if fetch:
            tiktok_account = await TikTokAccount.fetch(username)
            return tiktok_account

    @staticmethod
    async def get(username: str, fetch=True):
        """Get a TikTokAccount object.

        If the TikTokAccount object does not exist in cache, it will fetch it from the API.
        :param username: str
            The TikTok account username.
        :param fetch: bool
            Whether to fetch from the API if not found in cache.
        :returns: Optional[:ref:`TikTokAccount`]
            The TikTokAccount object requested.
        """
        username = username.lower()
        existing = _accounts.get(username)
        if not existing and fetch:
            return await TikTokAccount.fetch(username)
        return existing

    @staticmethod
    async def get_all():
        """
        Get all TikTokAccount objects in cache.

        :returns: dict_values[:ref:`TikTokAccount`]
            All TikTokAccount objects from cache.
        """
        return _accounts.values()

    @staticmethod
    async def fetch(username: str):
        """Fetch an updated TikTokAccount object from the API.

        :param username: int
            The TikTok account username to fetch.
        :returns: Optional[:ref:`TikTokAccount`]
            The TikTokAccount object requested.
        """
        return await internal_fetch(
            obj=TikTokAccount,
            request={
                "route": "tiktok/$username",
                "username": username,
                "method": "GET",
            },
        )

    @staticmethod
    async def fetch_all():
        """Fetch all TikTokAccount objects.

        .. NOTE:: TikTokAccount objects are added to cache on creation.
        """
        return await internal_fetch_all(
            obj=TikTokAccount, request={"route": "tiktok", "method": "GET"}, bulk=True
        )


_accounts: Dict[str, TikTokAccount] = dict()
