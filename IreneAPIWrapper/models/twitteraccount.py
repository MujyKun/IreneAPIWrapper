from typing import Optional, List, Dict

from . import (
    Subscription,
    Channel,
    Timeline,
    CallBack,
    Tweet,
    basic_call,
    internal_delete,
    internal_fetch,
    internal_fetch_all,
    internal_insert,
)
from IreneAPIWrapper.sections import outer

BASE_URL = "https://twitter.com"


class TwitterAccount(Subscription):
    """
    Represents a Twitter Account.

    A TwitterAccount object inherits from :ref:`Subscription`.

    Parameters
    ----------
    account_id: int
        The Twitter Account's ID.
    account_name: str
        The account's username.
    channels_following: Optional[List[:ref:`Channel`]]
        List of :ref:`Channel` objects that are following the Twitter Account.
    mention_roles: Optional[Dict[:ref:`Channel`, int]]
        Roles that are to be mentioned in a discord channel.

    Attributes
    ----------
    id: int
        Account ID.
    name: str
        The account's name.
    latest_tweet: Optional[:ref:`Tweet`]
        The latest tweet on the Twitter Account.
    """

    def __init__(
        self,
        account_id: int,
        account_name: str,
        channels_following: Optional[List[Channel]] = None,
        mention_roles: Optional[Dict[Channel, int]] = None,
    ):
        super().__init__(
            account_id=account_id,
            account_name=account_name,
            followed=channels_following,
            mention_roles=mention_roles,
        )

        # If the latest tweet does not exist, the first fetch will never be considered a new tweet.
        self._timeline: Timeline = Timeline(results=[])

        acc = _twitter_accounts.get(self.id)

        if not acc:
            # we need to make sure not to override the current object in cache.
            _twitter_accounts[self.id] = self
            _twitter_accounts_by_user[self.name] = self
        else:
            acc._sub_in_cache(channels=channels_following, role_ids=mention_roles)

    @property
    def latest_tweet(self) -> Optional[Tweet]:
        """Get the latest tweet."""
        return self._timeline.latest_tweet

    @staticmethod
    async def create(*args, **kwargs):
        """
        Create a TwitterAccount object.

        If several rows containing the same accounts are being passed in,
        use :ref:`create_bulk` instead for proper optimization.
        This will happen by default in a fallback if multiple rows are detected.

        :returns: Union[:ref:`TwitterAccount`, Optional[List[:ref:`TwitterAccount`]]]
        """
        # if a bundle of accounts is sent in, create them all.
        if not kwargs.get("accountid"):
            if len(kwargs.keys()) == 1:
                return await TwitterAccount.create(**kwargs["0"])

            return await TwitterAccount.create_bulk(list(kwargs.values()))

        account_id = kwargs.get("accountid")
        username = kwargs.get("username")
        channel_id = kwargs.get("channelid")
        guild_id = kwargs.get("guildid")

        channel = await Channel.get(channel_id)
        if not channel:
            await Channel.insert(channel_id, guild_id=guild_id)
            channel = await Channel.get(channel_id)

        if not channel.guild_id:
            channel.guild_id = guild_id

        role_id = kwargs.get("roleid")

        TwitterAccount(account_id, username, [channel], dict({channel: role_id}))
        return _twitter_accounts[account_id]

    @staticmethod
    async def create_bulk(list_of_dicts: List[dict]):
        """Bulk create TwitterAccount objects.

        :param list_of_dicts: List[dict]
            A list of dictionaries.
        :returns: Optional[List[:ref:`TwitterAccount`]]
        """
        final_channels = {}
        final_roles = {}
        for _dictionary in list_of_dicts:
            account_id = _dictionary["accountid"]
            username = _dictionary["username"]
            guild_id = _dictionary["guildid"]
            channel_id = _dictionary["channelid"]
            role_id = _dictionary["roleid"]

            channel = await Channel.get(channel_id)
            if not channel:
                await channel.insert(channel_id, guild_id)
                channel = await Channel.get(channel_id)

            if not channel.guild_id:
                channel.guild_id = guild_id

            if not final_channels.get(account_id):
                final_channels[account_id] = {
                    "channels": [channel],
                    "username": username,
                }
            else:
                final_channels[account_id]["channels"].append(channel)

            if role_id:
                if not final_roles.get(account_id):
                    final_roles[account_id] = dict({channel: role_id})
                else:
                    final_roles[account_id][channel] = role_id

        final_twitter_channels = []
        for _account_id, _values in final_channels.items():
            TwitterAccount(
                _account_id,
                _values["username"],
                _values["channels"],
                final_roles.get(_account_id),
            )
            obj = await TwitterAccount.get(_values["username"], fetch=False)
            final_twitter_channels.append(obj)

        return final_twitter_channels

    async def delete(self):
        """Delete Twitter account and it's followings."""
        for channel in self:
            await self.unsubscribe(channel)
        await self._remove_from_cache()

    async def fetch_timeline(self) -> Timeline:
        """Fetch the latest tweets for this account from Twitter"""
        callback = await basic_call(
            request={
                "route": "twitter/$twitter_id",
                "twitter_id": self.id,
                "method": "GET",
            }
        )
        results = callback.response["results"]
        if isinstance(results, list) and results:
            self._timeline.update_tweets(results)
        elif isinstance(results, dict):
            if results.get("title") and results['title'] == "Authorization Error":
                await self.delete()
        return self._timeline

    async def unsubscribe(self, channel: Channel):
        """
        Have a channel unsubscribe from the account if it is not already.

        :param channel: :ref:`Channel`
            The channel to unsubscribe from the account.
        """
        if channel not in self:
            return

        await basic_call(
            request={
                "route": "twitter/modify/$twitter_id",
                "twitter_id": self.id,
                "channel_id": channel.id,
                "method": "DELETE",
            }
        )
        self._unsub_in_cache(channel)

    async def subscribe(self, channel: Channel, role_id=None):
        """
        Have a channel subscribe to the account if it is not already.

        :param channel: The channel to subscribe to the account.
        :param role_id: The role id to mention.
        """
        if channel in self:
            # check for a role id update
            if await self.get_role_id(channel) != role_id:
                # unsubscribe them, then we resubscribe with the new role id.
                await self.unsubscribe(channel)
            else:
                return

        await basic_call(
            request={
                "route": "twitter/modify/$twitter_id",
                "twitter_id": self.id,
                "channel_id": channel.id,
                "role_id": role_id,
                "method": "POST",
            }
        )
        self._sub_in_cache(channel, role_id=role_id)

    async def _remove_from_cache(self) -> None:
        """
        Remove the TwitterAccount object from cache.

        :returns: None
        """
        _twitter_accounts.pop(self.id)

    @staticmethod
    async def subbed_in(guild_id):
        """
        Get the Twitter channels subscribed to in a Guild.

        :param guild_id: The guild ID.
        :return: Optional[List[:ref:`TwitterAccount`]]
        """
        return await internal_fetch_all(
            TwitterAccount,
            request={
                "route": "twitter/filter/$guild_id",
                "guild_id": guild_id,
                "method": "GET",
            },
        )

    @staticmethod
    async def check_user_exists(username) -> bool:
        """
        Check if a Twitter username exists.

        :param username: The Twitter display username.
        :return: bool
            Whether the username exists.
        """
        callback = await basic_call(
            request={
                "route": "twitter/exists/$username",
                "username": username,
                "method": "GET",
            }
        )
        return callback.response["results"]

    @staticmethod
    async def get_twitter_id(username) -> Optional[int]:
        """
        Get the Twitter account id of a username if it exists.

        :param username: The Twitter display username.
        :return: Optional[int]
            The account ID.
        """
        callback = await basic_call(
            request={
                "route": "twitter/account/$username",
                "username": username,
                "method": "POST",
            }
        )

        results = callback.response.get("results")
        if not results:
            return None

        return results.get("twitter_id")

    @staticmethod
    async def insert(
        username: str, guild_id: int, channel_id: int, role_id: Optional[int]
    ):
        """
        Insert a new TwitterAccount into the database.

        :param username: int
            The TwitterAccount username.
        :param guild_id: int
            The first guild ID that is subscribing.
        :param channel_id: int
            The first channel id that is subscribing.
        :param role_id: Optional[int]
            A role to notify.

        :return: :ref:`TwitterAccount`
            The TwitterAccount object.
        """
        username = username.lower()
        twitter_id = await TwitterAccount.get_twitter_id(username)
        if not twitter_id:
            return None

        await internal_insert(
            request={
                "route": "twitter/modify/$twitter_id",
                "twitter_id": twitter_id,
                "channel_id": channel_id,
                "role_id": role_id,
                "method": "POST",
            }
        )

        # have the model created and added to cache.
        twitter_account = await TwitterAccount.fetch(username)
        return twitter_account

    @staticmethod
    async def get(username: str = None, fetch=True) -> Optional[Subscription]:
        """
        Get a TwitterAccount instance from cache or fetch it from the api.

        :param username: str
            The username of the Twitter account.
        :param fetch: bool
            Whether to fetch from the API if not found in cache.
        :return: Optional[:ref:`TwitterAccount`]
            The TwitterAccount object.
        """
        username = username.lower()
        existing = _twitter_accounts_by_user.get(username)
        if not existing and fetch:
            return await TwitterAccount.fetch(username=username)
        return existing

    @staticmethod
    async def get_all():
        """
        Get all TwitterAccount objects in cache.

        :returns: dict_values[:ref:`TwitterAccount`]
            All TwitterAccount objects from cache.
        """
        return _twitter_accounts.values()

    @staticmethod
    async def fetch(username: str):
        """Fetch an updated TwitterAccount object from the API.

        :param username: int
            The Twitter account username to fetch.
        :returns: Optional[:ref:`TwitterAccount`]
            The TwitterAccount object requested.
        """
        return await internal_fetch(
            obj=TwitterAccount,
            request={
                "route": "twitter/$username",
                "username": username,
                "method": "GET",
            },
        )

    @staticmethod
    async def fetch_all():
        """
        Fetch all TwitterAccounts objects from the database.

        :return: List[:ref:`TwitterAccount`]
            A list of TwitterAccount objects.
        """
        return await internal_fetch_all(
            TwitterAccount, request={"route": "twitter/", "method": "GET"}, bulk=True
        )


_twitter_accounts: Dict[int, TwitterAccount] = dict()
_twitter_accounts_by_user: Dict[
    str, TwitterAccount
] = dict()  # used for faster searching.
