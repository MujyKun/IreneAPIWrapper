from typing import Optional, List

from . import Subscription, Channel

BASE_URL = "https://twitter.com"


class TwitterChannel(Subscription):
    def __init__(self,  account_name: str, followed: Optional[List[Channel]] = None):
        """
        Represents a Twitter Channel.
        :param account_name: ID of the Twitter Channel (The channel username)
        :param followed: List of discord channels that are following the Twitter channel.
        """
        super().__init__(account_name, followed)

        # If the latest content is None, we will just override it and not consider the first fetch as a new tweet.
        self.latest_tweet = None

    async def fetch_update(self) -> Optional[str]:
        """Fetch the latest tweet for this account from Twitter"""
        # TODO: make api request

        return ""

    async def validate(self) -> bool:
        """Checks if the Twitter ID (Channel Username) exists.

        :returns: (bool) Whether the Twitter channel exists.
        """
        # TODO: make api request

        return False