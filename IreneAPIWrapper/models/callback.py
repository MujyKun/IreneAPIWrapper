from random import randint
from typing import Dict, Optional
from datetime import datetime
import asyncio


class CallBack:
    def __init__(self, callback_type: str = "request", request: dict = None):
        """
        A call to the API and the request/response.

        :param callback_type: (str) Can be a 'request' or a 'disconnect'.
         """
        self.type = callback_type  # can be 'request' or 'disconnect'
        self._creation_time = datetime.now()
        self.id = request.get('callback_id') or self._get_unused_callback_id()
        callbacks[self.id] = self
        self.done = False
        self.request: Optional[dict] = request  # request data
        self.response: Optional[dict] = None  # data received from API
        self._completion_time = None
        self._expected_result = None  # used for testing.

    async def wait_for_completion(self):
        while True:
            await asyncio.sleep(0)
            if self.done:
                self._completion_time = datetime.now()
                return True

    def set_as_done(self):
        """Set the current callback as finished and lease the callback id to another object."""
        self.done = True
        # callbacks.pop(self.id)

    @staticmethod
    def _get_unused_callback_id() -> int:
        """Get an unused callback id."""
        while True:
            callback_id = int(f"{randint(0, 50000)}{datetime.utcnow().strftime('%Y%m%d%H%M%S')}")
            existing_callback = callbacks.get(callback_id)
            if existing_callback:
                continue
            return callback_id


callbacks: Dict[int, CallBack] = dict()
