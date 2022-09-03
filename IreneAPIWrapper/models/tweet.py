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

    def __eq__(self, other):
        return self.id == other.id

    def __hash__(self):
        return hash(self.id)
