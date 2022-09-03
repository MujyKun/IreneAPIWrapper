from typing import List, Optional

from . import Tweet


class Timeline:
    r"""
    Represents a Twitter Account's Timeline and contains a list of :ref:`Tweet` objects.

    Parameters
    ----------
    results: List[dict]
        The results from the API containing a list of dicts that contain the ID and text of the Tweet.

    Attributes
    ----------
    tweets: List[:ref:`Tweet`]
        A list of tweets.
    latest_tweet: Optional[:ref:`Tweet`]
        The latest tweet.
    """

    def __init__(self, results: List[dict], *args, **kwargs):
        """
        Represents a Twitter account's timeline and contains a list of tweets.
        """
        self.tweets: List[Tweet] = []
        self.new_tweets: List[Tweet] = []
        self.update_tweets(results)

    @property
    def latest_tweet(self) -> Optional[Tweet]:
        """Get the latest tweet."""
        return self[-1]

    def update_tweets(self, results: List[dict]):
        """Update the list of tweets with information from the API."""
        result_tweets = [Tweet(result["id"], result["text"]) for result in results]
        new_tweets = self.new_tweets + [
            tweet for tweet in result_tweets if tweet not in self.tweets
        ]
        # we only consider a tweet new if older tweets were present beforehand.
        self.new_tweets = new_tweets if self.tweets else []
        # confirm no duplicates.
        self.tweets = list(set(self.tweets + new_tweets))

    def __iter__(self):
        return self.tweets.__iter__()

    def __getitem__(self, item) -> Optional[Tweet]:
        try:
            tweet = self.tweets[item]
            return tweet
        except IndexError as e:
            return None
