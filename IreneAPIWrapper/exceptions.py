from .models import CallBack


class InvalidToken(Exception):
    """An Exception Raised When an Invalid Token was Supplied."""
    def __init__(self):
        super(InvalidToken, self).__init__("An Invalid Bearer Token was Supplied to IreneAPI.")


class APIError(Exception):
    """An Exception Raised When the API returned an error."""
    def __init__(self, callback: CallBack):
        self.callback = callback
        super(APIError, self).__init__(f"IreneAPI has returned back an error for Callback ID: {self.callback.id}.")
