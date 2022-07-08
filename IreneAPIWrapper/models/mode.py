class Mode:
    r"""
    Represents the Modes for certain entities.

    Please note that these Mode values are consistent across the API as well.

    Attributes
    ----------
    id: int
        The representative mode ID.
    name: str
        The name of the mode.

    """

    def __init__(self, access_id: int, name: str):
        self.id = access_id
        self.name = name


# PRE DEFINED MODES
NORMAL = Mode(1, "Normal")
GROUP = Mode(2, "Group")
