import asyncio
import aiohttp
from exceptions import InvalidToken
from typing import Union, Optional


class IreneAPIClient:
    r"""
    Asynchronous IreneAPI Client connected by a websocket.

    Parameters
    ----------
    token: str
        The API token provided.
    user_id: str
        The id of the user that has access to that token.

    """
    def __init__(self, token: str, user_id: Union[int, str]):
        self._ws_client: Optional[aiohttp.ClientSession] = None
        self._headers = {
            'Authorization': f'Bearer {token}',
            'user_id': str(user_id)
        }
        self._base_url = "localhost"
        self._base_port = 5454
        self._ws_url = f"ws://{self._base_url}:{self._base_port}/ws"
        self._queue = asyncio.Queue()
        # asyncio.run_coroutine_threadsafe(self.connect, loop)

        from test import run
        asyncio.run_coroutine_threadsafe(run(self), loop)

        self._disconnect = dict({'disconnect': True})

    async def _add_to_queue(self, body: dict):
        """
        Add a request to the queue.

        :param body: The request to send to the server.
        """
        await self._queue.put(body)

    async def connect(self):
        """
        Connect to the API via a websocket indefinitely.
        """
        if not self._ws_client:
            self._ws_client = aiohttp.ClientSession()

        try:
            async with self._ws_client.ws_connect(self._ws_url, headers=self._headers) as ws:
                while True:
                    # wait for a request.
                    data = await self._queue.get()

                    if data == self._disconnect:
                        await self._ws_client.close()
                        break  # close out of the session.

                    # make client request.
                    await ws.send_json(data)

                    # get response from server.
                    body = (await ws.receive()).data

                    print(body)
        except aiohttp.WSServerHandshakeError:
            raise InvalidToken

    async def disconnect(self):
        """
        Disconnect from the current websocket connection.
        """
        if not self._ws_client or self._ws_client.closed:
            return
        else:
            await self._add_to_queue(self._disconnect)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    try:
        # connect to db.
        t_token = "test"
        t_user_id = 169401247374376960
        client = IreneAPIClient(t_token, t_user_id)
        loop.run_until_complete(client.connect())
    except KeyboardInterrupt:
        ...
        print("interrupt")
        # loop.run_until_complete(self.close())
        # cancel all tasks lingering
    finally:
        loop.close()
