import logging

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
    verbose: bool
        Whether to print verbose messages.
    origin: str
        The origin meant for CORS to not return a bad request.
    logger: logging.Logger
        A logging object for messages to be sent to.
    """

    def __init__(
            self,
            token: str,
            user_id: Union[int, str],
            api_url="localhost",
            port=5454,
            preload_cache: Preload = None,
            test=False,
            reconnect=True,
            verbose=False,
            origin="localhost",
            logger: logging.Logger = None,
    ):
        ref_outer_client.client = self  # set our referenced client.
        self._ws_client: Optional[aiohttp.ClientSession] = None

        self.connected = False

        self._headers = {"Authorization": f"Bearer {token}", "Origin": origin}

        self._query_params = {"user_id": user_id}

        self._base_url = api_url.replace("http://", "").replace("https://", "").lower() or "localhost"
        self._base_port = port or 5454

        if "127.0.0.1" in self._base_url or "localhost" in self._base_url:
            self._ws_url = f"ws://{self._base_url}:{self._base_port}/ws"
        else:
            self._ws_url = f"https://{self._base_url}/ws"
        self._queue = asyncio.Queue()
        # asyncio.run_coroutine_threadsafe(self.connect, loop)

        self._disconnect = dict({"disconnect": True})

        self._preload_cache = preload_cache or Preload()

        self.in_testing = test
        self.reconnect = reconnect
        self.logger: Logger = Logger(verbose=verbose, logger=logger)
        self.__futures: list = []

    @property
    def is_preloaded(self):
        """Check if the client is preloaded with cache."""
        # if there are any futures not done, return False
        return not any([not future.done() for future in self.__futures])

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
            raise APIError(callback, detailed_report=True, error_msg="No Response was received.")
        if callback.response.get("error"):
            raise APIError(callback, error_msg=callback.response.get("error"))

        try:
            if callback.response.get("results"):
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
        self.__futures = []

        for category_class, load_cache in dict(sorted(evaluation.items(),
                                                      key=lambda model: model[0].priority())).items():
            try:
                if load_cache:
                    if self._preload_cache.force:
                        await category_class.fetch_all()
                    else:
                        self.__futures.append(asyncio.run_coroutine_threadsafe(
                            category_class.fetch_all(), loop
                        ))
            except Exception as e:
                self.logger.warning(msg=f"Cache for {category_class.__name__} did not load. - {e}")

    async def connect(self):
        """
        Connect to the API via a websocket indefinitely.
        """
        while True:
            try:
                await self._connect()
            except ConnectionResetError:
                if self.connected:
                    self.logger.error("Connection to IreneAPI Dropped.")
                    self.connected = False
                if self.reconnect:
                    self.logger.info("Attempting to reconnect to IreneAPI.")
                    continue
                else:
                    break
            except Exception as e:
                self.logger.error(f"API Connection Dropped: {e}")
        self.connected = False

    async def _connect(self):
        """
        Connect to the API via a websocket indefinitely.
        """
        if not self._ws_client:
            self._ws_client = aiohttp.ClientSession()

        try:
            async with self._ws_client.ws_connect(
                    self._ws_url,
                    headers=self._headers,
                    params=self._query_params,
                    max_msg_size=1073741824,
                    timeout=60,
            ) as ws:
                self.connected = True
                self.logger.info("Connected to IreneAPI.")

                if self._preload_cache.force:
                    asyncio.run_coroutine_threadsafe(self.__load_up_cache(), asyncio.get_event_loop())
                else:
                    await self.__load_up_cache()

                no_found_instance = f"Could not find CallBack instance"
                while True:
                    # test cases
                    if self.in_testing and self._queue.empty():
                        # pass if the api is using a debugger so the session does not close.
                        # pass
                        await self._ws_client.close()
                        return  # close out of the session.

                    # wait for a request.
                    callback: CallBack = await self._queue.get()

                    if callback.type == "disconnect":
                        await self._ws_client.close()
                        return  # close out of the session.

                    # make client request.
                    await ws.send_json(callback.request)

                    # get response from server.
                    # in case of any inconsistencies, a callback id is sent back and forth and is checked for
                    # authenticity before completing a request.
                    _data = await ws.receive()
                    if _data is None:
                        self.logger.warning(
                            no_found_instance + ": Received data was NoneType."
                        )
                        continue
                    elif isinstance(_data, aiohttp.WSMessage) and _data.type == aiohttp.WSMsgType.CLOSE:
                        self.logger.warning(
                            f"Received WSMsgType.Close"
                        )
                        continue

                    data_response = _data.json()

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
                        self.logger.warning(f"{no_found_instance}: {data_response}")
        except aiohttp.WSServerHandshakeError:
            raise InvalidToken
        except (ConnectionResetError, aiohttp.ClientConnectorError):
            raise ConnectionResetError
        except KeyboardInterrupt:
            self.connected = False
        except Exception as e:
            self.logger.error(f"API Connection Dropped - {e}")
            raise ConnectionResetError

    async def disconnect(self):
        """
        Disconnect from the current websocket connection.
        """
        if not self._ws_client or self._ws_client.closed:
            return
        else:
            callback = CallBack(callback_type="disconnect", request=self._disconnect)
            await self.add_to_queue(callback)


class Logger:
    """
    A logger to allow for simpler referencing and checks.

    Parameters
    ----------
    verbose: bool
        Whether to print verbose messages.
    logger: logging.Logger
        A logging object for messages to be sent to.

    Attributes
    ----------
    verbose: bool
        Whether to print verbose messages.
    logger: logging.Logger
        A logging object for messages to be sent to.
    """

    def __init__(self, verbose=False, logger=None):
        self.verbose = verbose
        self.logger: Optional[logging.Logger] = logger

    def warning(self, msg, *args, **kwargs):
        self.print(msg)
        if self.logger:
            self.logger.warning(msg)

    def info(self, msg, *args, **kwargs):
        self.print(msg)
        if self.logger:
            self.logger.info(msg)

    def error(self, msg, *args, **kwargs):
        self.print(msg)
        if self.logger:
            self.logger.error(msg)

    def print(self, msg):
        if self.verbose:
            print(msg)
