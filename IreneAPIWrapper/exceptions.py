from .models import CallBack


class InvalidToken(Exception):
    """An Exception Raised When an Invalid Token was Supplied."""

    def __init__(self):
        super(InvalidToken, self).__init__(
            "An Invalid Bearer Token was Supplied to IreneAPI."
        )


class APIError(Exception):
    """An Exception Raised When the API returned an error."""

    def __init__(self, callback: CallBack, error_msg=None, detailed_report=False):
        self.callback = callback
        self.error_msg = error_msg
        # do not simplify this condition. get_detailed_report utilizes self.error_msg, so it must exist prior.
        if detailed_report:
            self.get_detailed_report()
        super(APIError, self).__init__(
            f"IreneAPI has returned back an error for Callback ID: {self.callback.id}.\n "
            f"Error Message: {self.error_msg}"
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


class IncorrectNumberOfItems(Exception):
    """An Exception caused when there is not enough or too much
    of something (for example arguments)."""

    def __init__(self, msg):
        super(IncorrectNumberOfItems, self).__init__(msg)


class FailedObjectCreation(Exception):
    """An exception caused when objects failed to properly create."""

    def __init__(self, callback):
        self.callback = callback
        super(FailedObjectCreation, self).__init__()
