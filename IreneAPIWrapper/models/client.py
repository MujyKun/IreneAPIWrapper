import aiohttp
import asyncio
from IreneAPIWrapper.exceptions import InvalidToken, APIError
from IreneAPIWrapper.sections import outer as ref_outer_client
from typing import Union, Optional
from IreneAPIWrapper.models import CallBack, callbacks


class IreneAPIClient:
    r"""
    Asynchronous IreneAPI Client connected by a websocket.

    .. Warning::
        It is suggested to only create ONE client per application. The wrapper externally
        references the latest client created. If it is several clients that are routing to the same API,
        then it is okay as the same requests will be sent; otherwise, it can lead to conflicts between databases.

    Attributes
    ----------
    token: str
    user_id: Union[int, str]
    api_url: str
        Defaults to localhost. Websocket URL is expected to be ws://{api_url}:{port}/ws.
    port: int
        The api port.
    load_all_tags: bool
        Whether to preload all cache for tags.
    load_all_person_aliases: bool
        Whether to preload all cache for person_aliases.
    load_all_group_aliases: bool
        Whether to preload all cache for group_aliases.
    load_all_persons: bool
        Whether to preload all cache for persons.
    load_all_groups: bool
        Whether to preload all cache for groups.
    load_all_twitter_accounts: bool
        Whether to preload all cache for twitter_accounts.
    load_all_users: bool
        Whether to preload all cache for users.
    load_all_guilds: bool
        Whether to preload all cache for guilds.
    load_all_affiliations: bool
        Whether to preload all cache for affiliations.
    load_all_bloodtypes: bool
        Whether to preload all cache for bloodtypes.
    load_all_media: bool
        Whether to preload all cache for media.
    load_all_displays: bool
        Whether to preload all cache for displays.
    load_all_companies: bool
        Whether to preload all cache for companies.
    load_all_dates: bool
        Whether to preload all cache for dates.
    load_all_locations: bool
        Whether to preload all cache for locations.
    load_all_positions: bool
        Whether to preload all cache for positions.
    load_all_socials: bool
        Whether to preload all cache for socials.
    load_all_fandoms: bool
        Whether to preload all cache for fandoms.
    test: bool
        Whether to go into test/dev mode. Does not currently have a significant difference.

    Parameters
    ----------
    token: str
        The API token provided.
    user_id: str
        The id of the user that has access to that token.
    connected: bool
        If there is a stable websocket connection to the API.
    in_testing: bool
        Whether the Client is in testing mode.

    """

    def __init__(
        self,
        token: str,
        user_id: Union[int, str],
        api_url="localhost",
        port=5454,
        load_all_tags=True,
        load_all_person_aliases=True,
        load_all_group_aliases=True,
        load_all_persons=True,
        load_all_groups=True,
        load_all_twitter_accounts=True,
        load_all_users=False,
        load_all_guilds=False,
        load_all_affiliations=True,
        load_all_bloodtypes=True,
        load_all_media=True,
        load_all_displays=True,
        load_all_companies=True,
        load_all_dates=True,
        load_all_locations=True,
        load_all_positions=True,
        load_all_socials=True,
        load_all_fandoms=True,
        load_all_channels=False,
        test=False,
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

        from . import (
            Tag,
            PersonAlias,
            GroupAlias,
            Affiliation,
            BloodType,
            Media,
            Display,
            Company,
            Date,
            Location,
            Position,
            Social,
            Person,
            TwitterAccount,
            User,
            Channel,
            Group,
            Fandom,
            Guild,
        )

        self.__cache_preload = {
            Tag: load_all_tags,
            PersonAlias: load_all_person_aliases,
            GroupAlias: load_all_group_aliases,
            Affiliation: load_all_affiliations,
            BloodType: load_all_bloodtypes,
            Media: load_all_media,
            Display: load_all_displays,
            Company: load_all_companies,
            Date: load_all_dates,
            Location: load_all_locations,
            Position: load_all_positions,
            Social: load_all_socials,
            Fandom: load_all_fandoms,
            Person: load_all_persons,
            Group: load_all_groups,
            TwitterAccount: load_all_twitter_accounts,
            User: load_all_users,
            Guild: load_all_guilds,
            Channel: load_all_channels,
        }

        self.in_testing = test

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
        if callback.response.get("error"):
            raise APIError(callback, error_msg=callback.response.get("error"))

        try:
            if callback.response.get('results'):
                error = callback.response["results"][
                    "error"
                ]  # forcing a KeyError (if raised, is a success)
                raise APIError(callback, error_msg=error)
        except KeyError:
            pass

    async def __load_up_cache(self):
        """
        Preload the cache based on client preferences.

        .. NOTE::: If an object is dependent on another object, it will create the other object.
        """
        loop = asyncio.get_event_loop()
        for category_class, load_cache in self.__cache_preload.items():
            asyncio.run_coroutine_threadsafe(category_class.fetch_all(), loop)

    async def connect(self):
        """
        Connect to the API via a websocket indefinitely.
        """
        if not self._ws_client:
            self._ws_client = aiohttp.ClientSession()

        try:
            async with self._ws_client.ws_connect(
                self._ws_url, headers=self._headers, params=self._query_params
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
