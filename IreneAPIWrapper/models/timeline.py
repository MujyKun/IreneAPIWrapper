from typing import List

from . import Tweet


class Timeline:
    r"""
    Represents a Twitter Account's Timeline and contains a list of :ref:`Twwet`s

    Attributes
    ----------
    tweets: List[:ref:`Tweet`]
        A list of tweets.
    """
    def __init__(self, *args, **kwargs):
        """
        Represents a Twitter account's timeline and contains a list of tweets.
        """
        self.tweets: List[Tweet] = []

    def __iter__(self):
        return self.tweets.__iter__()
