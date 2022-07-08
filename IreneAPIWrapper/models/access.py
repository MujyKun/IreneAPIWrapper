class Access:
    r"""
    Represents the Access level of the API.

    Please note that these Access values are consistent across the API as well.

    Attributes
    ----------
    id: int
        The representative Access ID.

    """

    def __init__(self, access_id: int):
        self.id = access_id


# PRE DEFINED ACCESS
GOD = Access(-1)
OWNER = Access(0)
DEVELOPER = Access(1)
SUPER_PATRON = Access(2)
FRIEND = Access(3)
USER = Access(4)
