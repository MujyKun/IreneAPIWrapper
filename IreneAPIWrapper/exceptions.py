from .models import CallBack


class InvalidToken(Exception):
    """An Exception Raised When an Invalid Token was Supplied."""

    def __init__(self):
        super(InvalidToken, self).__init__(
            "An Invalid Bearer Token was Supplied to IreneAPI."
        )


class APIError(Exception):
    """An Exception Raised When the API returned an error."""

    def __init__(self, callback: CallBack, error_msg=None):
        self.callback = callback
        self.error_msg = error_msg
        super(APIError, self).__init__(
            f"IreneAPI has returned back an error for Callback ID: {self.callback.id}.\n "
            f"Error Message: {error_msg}"
        )

    def get_detailed_report(self):
        from pprint import pformat
        cb = self.callback
        msg = f"""
        **CallBack Information**
        **--------------------------**
        **ID:** {cb.id}

        **Request:** {pformat(cb.request)}

        **Response:** {pformat(cb.response)}

        **Type:** {cb.type}

        **Done (Flag):** {cb.done}

        **Error Message:** {pformat(self.error_msg)}
        """
        return msg


class Empty(Exception):
    """An exception caused when an iterable is empty."""

    def __init__(self):
        super(Empty, self).__init__()
