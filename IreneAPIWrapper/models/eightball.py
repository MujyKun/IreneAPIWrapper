from typing import Union, List, Optional, Dict

from . import (
    AbstractModel,
    internal_fetch,
    internal_fetch_all,
    internal_delete,
    internal_insert,
)
from random import choice


class EightBallResponse(AbstractModel):
    r"""Represents an eight-ball Response.

    An EightBallResponse object inherits from :ref:`AbstractModel`.

    Parameters
    ----------
    response_id: int
        The response id.
    response: str
        The response itself.

    Attributes
    ----------
    id: int
        The response id.
    response: str
        The response itself.

    """

    def __init__(
        self,
        response_id: int,
        response: str,
    ):
        super(EightBallResponse, self).__init__(response_id)
        self.response: str = response

        if not _responses.get(self.id):
            # we need to make sure not to override the current object in cache.
            _responses[self.id] = self

    @staticmethod
    async def create(*args, **kwargs):
        """
        Create an EightBallResponse object.

        :returns: :ref:`EightBallResponse`
        """
        response_id = kwargs.get("responseid")
        response = kwargs.get("response")

        EightBallResponse(response_id, response)
        return _responses[response_id]

    async def delete(self) -> None:
        """
        Delete the Response object from the database and remove it from cache.

        :returns: None
        """
        await internal_delete(
            self,
            request={
                "route": "8ball/$response_id",
                "response_id": self.id,
                "method": "DELETE",
            },
        )
        await self._remove_from_cache()

    async def _remove_from_cache(self) -> None:
        """
        Remove the EightBallResponse object from cache.

        :returns: None
        """
        _responses.pop(self.id)

    @staticmethod
    async def insert(response: str) -> None:
        """
        Insert a new EightBallResponse into the database and cache.

        :param response: str
            Response Message.
        """
        callback = await internal_insert(
            request={
                "route": "8ball",
                "response": response,
                "method": "POST",
            }
        )

    @staticmethod
    async def get(response_id: int, fetch=True):
        """Get an EightBallResponse object.

        If the EightBallResponse object does not exist in cache, it will fetch the object from the API.
        :param response_id: int
            The ID of the Response to get/fetch.
        :param fetch: bool
            Whether to fetch from the API if not found in cache.
        :returns: Optional[:ref:`EightBallResponse`]
            The EightBallResponse object requested.
        """
        existing = _responses.get(response_id)
        if not existing and fetch:
            return await EightBallResponse.fetch(response_id)
        return existing

    @staticmethod
    async def get_all():
        """
        Get all EightBallResponse objects in cache.

        :returns: dict_values[:ref:`EightBallResponse`]
            All EightBallResponse objects from cache.
        """
        return _responses.values()

    @staticmethod
    async def get_random_response(fetch=False):
        """
        Get a random response

        :param fetch: bool
            Whether to fetch fresh results from the API.
        :return: :ref:`EightBallResponse`
            A random response object.
        """
        if fetch:
            await EightBallResponse.fetch_all()
        return choice(list(_responses.values()))

    @staticmethod
    async def fetch(response_id: int):
        """Fetch an updated EightBallResponse object from the API.

        .. NOTE:: EightBallResponse objects are added to cache on creation.

        :param response_id: int
            The response's ID to fetch.
        :returns: Optional[:ref:`EightBallResponse`]
            The EightBallResponse object requested.
        """
        return await internal_fetch(
            obj=EightBallResponse,
            request={
                "route": "8ball/$response_id",
                "response_id": response_id,
                "method": "GET",
            },
        )

    @staticmethod
    async def fetch_all():
        """Fetch all responses.

        .. NOTE:: EightBallResponse objects are added to cache on creation.
        """
        return await internal_fetch_all(
            obj=EightBallResponse, request={"route": "8ball", "method": "GET"}
        )


_responses: Dict[int, EightBallResponse] = dict()
