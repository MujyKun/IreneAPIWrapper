class Access:
    def __init__(self, access_id: int):
        self.id = access_id


# PRE DEFINED ACCESS
GOD = Access(-1)
OWNER = Access(0)
DEVELOPER = Access(1)
SUPER_PATRON = Access(2)
FRIEND = Access(3)
USER = Access(4)
