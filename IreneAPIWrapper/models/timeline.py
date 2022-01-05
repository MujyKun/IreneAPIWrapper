from typing import List

from . import Tweet


class Timeline:
    def __init__(self, *args, **kwargs):
        """
        Represents a Twitter account's timeline and contains list of tweets.
        """
        self.tweets: List[Tweet] = []
