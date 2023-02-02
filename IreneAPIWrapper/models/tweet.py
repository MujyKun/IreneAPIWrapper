class Tweet:
    r"""
    Represents a Twitter Account's Tweet.

    Attributes
    ----------
    id: int
        The Tweet ID.
    content: str
        The Tweet's contents
    """

    def __init__(self, *args, **kwargs):
        self.id = args[0]
        self.text = args[1]

    @property
    def is_retweet(self) -> bool:
        """Whether the tweet is a retweet."""
        return self.text and self.text[:2] == 'RT'

    @property
    def is_reply(self) -> bool:
        """
        Whether the tweet is a reply (sometimes)

        ..Note:: Twitter sucks and doesn't let us know if it's a reply, so here we are filtering by if the user @ed
        someone at the start of their tweet...
        """
        return self.text and self.text[:1] == '@'

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)
