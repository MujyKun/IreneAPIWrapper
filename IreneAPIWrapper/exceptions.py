
class InvalidToken(Exception):
    """An Exception Raised When an Invalid Token was Supplied."""
    def __init__(self):
        super(InvalidToken, self).__init__("An Invalid Bearer Token was Supplied to IreneAPI.")

