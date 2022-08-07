import aiohttp
import asyncio
from IreneAPIWrapper.exceptions import InvalidToken, APIError
from IreneAPIWrapper.sections import outer as ref_outer_client
from typing import Union, Optional
from IreneAPIWrapper.models import CallBack, callbacks, Preload


class IreneAPIClient:
    r"""
    Asynchronous IreneAPI Client connected by a websocket.

    .. Warning::
        It is suggested to only create ONE client per application. The wrapper externally
        references the latest client created. If it is several clients that are routing to the same API,
        then it is okay as the same requests will be sent; otherwise, it can lead to conflicts between databases.

    Parameters
    ----------
    token: str
    user_id: Union[int, str]
    api_url: str
        Defaults to localhost. Websocket URL is expected to be ws://{api_url}:{port}/ws.
    port: int
        The api port.
    test: bool
        Whether to go into test/dev mode. Does not currently have a significant difference.
    reconnect: bool
        Whether to reconnect to the API if a connection is severed.

    Attributes
    ----------
    token: str
        The API token provided.
    user_id: str
        The id of the user that has access to that token.
    connected: bool
        If there is a stable websocket connection to the API.
    in_testing: bool
        Whether the Client is in testing mode.
    reconnect: bool
        Whether to reconnect to the API if a connection is severed. True by default.
    """

    def __init__(
        self,
        token: str,
        user_id: Union[int, str],
        api_url="localhost",
        port=5454,
        preload_cache: Preload = None,
        test=False,
        reconnect=True
    ):
        ref_outer_client.client = self  # set our referenced client.
        self._ws_client: Optional[aiohttp.ClientSession] = None

        self.connected = False

        self._headers = {"Authorization": f"Bearer {token}"}

        self._query_params = {"user_id": user_id}

        self._base_url = api_url or "localhost"
        self._base_port = port or 5454
        self._ws_url = f"ws://{self._base_url}:{self._base_port}/ws"
        self._queue = asyncio.Queue()
        # asyncio.run_coroutine_threadsafe(self.connect, loop)

        self._disconnect = dict({"disconnect": True})

        self._preload_cache = preload_cache or Preload()

        self.in_testing = test
        self.reconnect = reconnect

    async def add_to_queue(self, callback: CallBack):
        """
        Add a request to the queue.

        :param callback: :ref:`CallBack` The request to send to the server.
        """
        await self._queue.put(callback)

    async def add_and_wait(self, callback: CallBack):
        """
        Add a callback to the queue and wait for it to complete.

        :param callback: The callback to add to the queue and wait for.
        """
        await self.add_to_queue(callback)
        await callback.wait_for_completion()
        if callback.response is None:
            raise APIError(callback, detailed_report=True)
        if callback.response.get("error"):
            raise APIError(callback, error_msg=callback.response.get("error"))

        try:
            if callback.response.get('results'):
                error = callback.response["results"][
                    "error"
                ]  # forcing a KeyError/TypeError (if raised, is a success)
                raise APIError(callback, error_msg=error)
        except (KeyError, TypeError):
            pass

    async def __load_up_cache(self):
        """
        Preload the cache based on client preferences.

        .. NOTE::: If an object is dependent on another object, it will create the other object.
        """
        loop = asyncio.get_event_loop()
        evaluation = self._preload_cache.get_evaluation()
        for category_class, load_cache in evaluation.items():
            if load_cache:
                future = asyncio.run_coroutine_threadsafe(category_class.fetch_all(), loop)

    async def connect(self):
        """
        Connect to the API via a websocket indefinitely.
        """
        if not self._ws_client:
            self._ws_client = aiohttp.ClientSession()

        try:
            async with self._ws_client.ws_connect(
                self._ws_url, headers=self._headers, params=self._query_params, max_msg_size=1073741824, timeout=60
            ) as ws:
                self.connected = True
                await self.__load_up_cache()

                while True:
                    # test cases
                    if self.in_testing and self._queue.empty():
                        # pass if the api is using a debugger so the session does not close.
                        # pass
                        await self._ws_client.close()
                        break

                    # wait for a request.
                    callback: CallBack = await self._queue.get()

                    if callback.type == "disconnect":
                        await self._ws_client.close()
                        break  # close out of the session.

                    # make client request.
                    await ws.send_json(callback.request)

                    # get response from server.
                    # in case of any inconsistencies, a callback id is sent back and forth and is checked for
                    # authenticity before completing a request.
                    data_response = (await ws.receive()).json()

                    response_callback_id = int(data_response.get("callback_id") or 0)
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
                        # TODO: Remove Print
                        print(f"Could not find CallBack instance for: {data_response}")

        except aiohttp.WSServerHandshakeError:
            raise InvalidToken
        except (ConnectionResetError, aiohttp.ClientConnectorError):
            if self.reconnect:
                while True:
                    await self.connect()

        self.connected = False

    async def disconnect(self):
        """
        Disconnect from the current websocket connection.
        """
        if not self._ws_client or self._ws_client.closed:
            return
        else:
            callback = CallBack(callback_type="disconnect", request=self._disconnect)
            await self.add_to_queue(callback)
