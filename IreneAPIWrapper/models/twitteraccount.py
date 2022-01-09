from typing import Optional, List, Dict

from . import Subscription, Channel, Timeline, CallBack
from IreneAPIWrapper.sections import outer
BASE_URL = "https://twitter.com"


class TwitterAccount(Subscription):
    def __init__(self, account_id: int, account_name: str, followed: Optional[List[Channel]] = None):
        """
        Represents a Twitter Account.
        :param account_name: username of the Twitter Channel (The channel username)
        :param followed: List of discord channels that are following the Twitter channel.
        """
        super().__init__(account_id, account_name, followed)

        # If the latest content is None, we will just override it and not consider the first fetch as a new tweet.
        self.latest_tweet = None

    async def fetch_timeline(self) -> Timeline:
        """Fetch the latest tweets for this account from Twitter"""
        # TODO: make api request
        callback = CallBack(request={
            'route': 'twitter/timeline/$twitter_id',
            'twitter_id': self.id,
            'method': 'GET'}
        )

        await outer.client.add_and_wait(callback)
        return Timeline(**callback.response["results"])

    @staticmethod
    async def _fetch_all_subscriptions() -> CallBack:
        """
        Fetch all subscription information for all accounts.

        This returns the exact API Callback. This may only be useful internally.
        :return:
        """
        callback = CallBack(request={
            'route': 'twitter/subscriptions',
            'method': 'GET'}
        )

        await outer.client.add_and_wait(callback)
        return callback

    @staticmethod
    async def fetch_all() -> dict:
        """
        Fetch a dict of all Twitter accounts and subscriptions in the database.

        :return: (Dict[int, TwitterAccount]) A dictionary of TwitterAccount objects with the ID as the key.
        """

        callback = CallBack(request={
            'route': 'twitter/accounts',
            'method': 'GET'}
        )

        await outer.client.add_and_wait(callback)

        for key, acc_info in (callback.response["results"]).items():
            _twitter_accounts[acc_info["accountid"]] = TwitterAccount(acc_info["accountid"], acc_info["username"])

        subs_callback = await TwitterAccount._fetch_all_subscriptions()

        for key, sub_info in (subs_callback.response["results"]).items():
            channel = await Channel.get(sub_info["channelid"])
            _twitter_accounts[sub_info["accountid"]]._add_to_cache(channel, sub_info["roleid"])

        return _twitter_accounts

    async def remove(self):
        """
        Remove the current Twitter Account

        This will also remove all subscriptions permanently. Use with caution.
        """
        _twitter_accounts.pop(self.id)
        callback = CallBack(request={
            'route': 'twitter/$twitter_info',
            'account_id': self.id,
            'method': 'DELETE'}
        )
        await outer.client.add_and_wait(callback)

    async def unsubscribe(self, channel: Channel):
        """
        Have a channel unsubscribe from the account if it is not already.

        :param channel: (Channel) The channel to unsubscribe from the account.
        """
        if channel not in self:
            return

        callback = CallBack(request={
            'route': 'twitter/$twitter_id/$channel_id',
            'account_id': self.id,
            'channel_id': channel.id,
            'method': 'DELETE'}
        )

        await outer.client.add_and_wait(callback)
        self._remove_from_cache(channel)

        ...

    async def subscribe(self, channel: Channel, role_id=None):
        """
        Have a channel subscribe to the account if it is not already.

        :param channel: The channel to subscribe to the account.
        :param role_id: The role id to mention.
        """
        if channel in self:
            return

        request = {
            'route': 'twitter/$twitter_id/$channel_id',
            'account_id': self.id,
            'channel_id': channel.id,
            'method': 'POST'}

        if role_id:
            request['role_id'] = role_id

        callback = CallBack(request=request)

        await outer.client.add_and_wait(callback)
        self._add_to_cache(channel, role_id=role_id)

    @staticmethod
    async def get(username: str = None, account_id: int = None) -> Optional[Subscription]:
        """
        Get a TwitterAccount instance from cache or fetch it from the api.

        Will insert into the database if it does not already exist.
        Only pass in an account id if it is 100% certain it is in cache.

        :param username: The username of the Twitter account.
        :param account_id: The Twitter account ID.
        :return: (Subscription)
            The Subscription object.
        """
        if account_id:
            channel = _twitter_accounts.get(account_id)
            if channel:
                return channel

        if username:
            for channel in _twitter_accounts.values():
                if channel.name == username.lower():
                    return channel

            return await TwitterAccount.fetch(username=username)

        ...  # check local cache, then fetch/add

    @staticmethod
    async def fetch(username) -> Optional[Subscription]:
        """
        Fetch a TwitterAccount instance directly from the API.

        :param username: The username of the Twitter account.
        :return: (Subscription)
            The Subscription object.
        """
        callback = CallBack(request={
            'route': 'twitter/$twitter_info',
            'username': username,
            'method': 'POST'}
        )

        await outer.client.add_and_wait(callback)
        if callback.response.get("results"):
            account_id = callback.response["results"]["t_accountid"]
            account = TwitterAccount(account_id, username.lower())
            _twitter_accounts[account.id] = account
            return account


_twitter_accounts: Dict[int, TwitterAccount] = dict()
