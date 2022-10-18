from random import randint
from typing import Dict, Optional
from datetime import datetime, timedelta
import asyncio


class CallBack:
    r"""
    Represents a CallBack from the API (Request & Response).

    Parameters
    ----------
    callback_type: str
        The type of callback. Can be 'request' or 'disconnect'.
    request: Optional[dict]
        A request if it's already known.

    Attributes
    ----------
    id: int
        Is the CallBack ID. Consists of a random integer from 0 to 50,000 concatenated with the current timestamp.
    type: str
        The callback type. Can be 'request' or 'disconnect'.
    _creation_time: :ref:`datetime`
        The creation time of the object.
    done: bool
        Whether a response has been received.
    request: Optional[dict]
        The request to be sent to the API.
    response: Optional[dict]
        The response received from the API.
    _completion_time: :ref:`datetime`
        The time the response from the API was received.
    _expected_result: Optional[dict]
        Used for testing expected responses from the API.
    """

    def __init__(self, callback_type: str = "request", request: dict = None):
        self.type = callback_type  # can be 'request' or 'disconnect'
        self._creation_time = datetime.now()
        self.done = False
        self.request: Optional[dict] = request  # request data
        self.id = request.get("callback_id") or self._get_unused_callback_id()
        self.request["callback_id"] = self.id
        callbacks[self.id] = self
        self.response: Optional[dict] = None  # data received from API
        self._completion_time = None
        self._expected_result = None  # used for testing.

    async def wait_for_completion(self, timeout: Optional[int] = None) -> bool:
        r"""
        Waits for a response from the API.

        :param timeout: Optional[int]
            Seconds before no longer waiting for the response. (No timeout by default.)
        :returns: True
            Only returns when there is a response from the API.
        """
        end_time = None
        if timeout:
            end_time = datetime.now() + timedelta(seconds=timeout)
        while True:
            await asyncio.sleep(0)

            if self.done:
                self._completion_time = datetime.now()
                return True

            if timeout:
                if datetime.now() > end_time:
                    return False

    def set_as_done(self) -> None:
        """
        Set the current callback as finished.

        :returns: None
        """
        self.done = True

    @staticmethod
    def _get_unused_callback_id() -> int:
        """Get an unused callback id/name."""
        while True:
            callback_id = int(
                f"{randint(0, 50000)}{datetime.utcnow().strftime('%Y%m%d%H%M%S')}"
            )
            existing_callback = callbacks.get(callback_id)
            if existing_callback:
                continue
            return callback_id


callbacks: Dict[int, CallBack] = dict()
