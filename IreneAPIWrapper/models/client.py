import aiohttp
import asyncio
from IreneAPIWrapper.exceptions import InvalidToken, APIError
from IreneAPIWrapper.sections import outer as ref_outer_client
from typing import Union, Optional
from IreneAPIWrapper.models import CallBack, callbacks


class IreneAPIClient:
    r"""
    Asynchronous IreneAPI Client connected by a websocket.

    Parameters
    ----------
    token: str
        The API token provided.
    user_id: str
        The name of the user that has access to that token.

    """

    def __init__(self, token: str, user_id: Union[int, str], test=False):
        ref_outer_client.client = self  # set our referenced client.
        self._ws_client: Optional[aiohttp.ClientSession] = None

        self.connected = False

        self._headers = {
            'Authorization': f'Bearer {token}'
        }

        self._query_params = {
            'user_id': user_id
        }

        self._base_url = "localhost"
        self._base_port = 5454
        self._ws_url = f"ws://{self._base_url}:{self._base_port}/ws"
        self._queue = asyncio.Queue()
        # asyncio.run_coroutine_threadsafe(self.connect, loop)

        self._disconnect = dict({'disconnect': True})

        self.in_testing = test

    async def add_to_queue(self, callback: CallBack):
        """
        Add a request to the queue.

        :param callback: (CallBack) The request to send to the server.
        """
        await self._queue.put(callback)

    async def add_and_wait(self, callback: CallBack):
        """
        Add a callback to the queue and wait for it to complete.

        :param callback: The callback to add to the queue and wait for.
        """
        await self.add_to_queue(callback)
        await callback.wait_for_completion()
        if callback.response.get("error"):
            raise APIError(callback)

    async def connect(self):
        """
        Connect to the API via a websocket indefinitely.

        """
        if not self._ws_client:
            self._ws_client = aiohttp.ClientSession()

        try:
            async with self._ws_client.ws_connect(self._ws_url, headers=self._headers, params=self._query_params) as ws:
                self.connected = True

                while True:

                    # test cases
                    if self.in_testing and self._queue.empty():
                        # pass if the api is using a debugger so the session does not close.
                        # pass
                        await self._ws_client.close()
                        break

                    # wait for a request.
                    callback: CallBack = await self._queue.get()

                    if callback.type == 'disconnect':
                        await self._ws_client.close()
                        break  # close out of the session.

                    # make client request.
                    await ws.send_json(callback.request)

                    # get response from server.
                    # in case of any inconsistencies, a callback name is sent back and forth and is checked for
                    # authenticity before completing a request.
                    data_response = (await ws.receive()).json()
                    response_callback_id = int(data_response.get('callback_id') or 0)
                    if response_callback_id and (response_callback_id != callback.id):
                        # we replace the current callback with the response
                        callback = callbacks.get(response_callback_id)

                    if callback:
                        # we shouldn't be receiving a response without a callback name, but if we do
                        # then we will take care of it as if it is for the same request.
                        callback.response = data_response
                        # A method should already have the CallBack object,
                        # so we can now finish the callback and lease out the callback name to a new object.
                        callback.set_as_done()
                    else:
                        print(f"Could not find CallBack instance for: {data_response}")

        except aiohttp.WSServerHandshakeError:
            raise InvalidToken

        self.connected = False

    async def disconnect(self):
        """
        Disconnect from the current websocket connection.
        """
        if not self._ws_client or self._ws_client.closed:
            return
        else:
            callback = CallBack(callback_type='disconnect', request=self._disconnect)
            await self.add_to_queue(callback)
