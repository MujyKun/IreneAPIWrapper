from typing import Union, List, Optional, Dict

from IreneAPIWrapper.sections import outer
from . import (
    CallBack,
    Access,
    AbstractModel,
    internal_fetch,
    internal_fetch_all,
    internal_insert,
    internal_delete,
    basic_call,
)


class UserStatus(AbstractModel):
    r"""Represents a user's status in a game.

    A UserStatus object inherits from :ref:`AbstractModel`.

    Parameters
    ----------
    status_id: int
        The status ID.
    user_id: int
        The user id.
    score: int
        The score.


    Attributes
    ----------
    id: int
        The status ID.
    user_id: int
        The user id.
    score: int
        The score.

    """

    def __init__(self, status_id: int, user_id: int, score: int, *args, **kwargs):
        super(UserStatus, self).__init__(status_id)
        self.user_id = user_id
        self.score = score

        if not _statuses.get(self.id):
            _statuses[self.id] = self

    @staticmethod
    async def create(*args, **kwargs):
        """
        Create a :ref:`UserStatus` object.

        :returns: :ref:`UserStatus`
        """
        status_id = kwargs.get("statusid")
        user_id = kwargs.get("userid")
        score = kwargs.get("score")
        UserStatus(status_id, user_id, score)

        return _statuses[status_id]

    async def delete(self) -> None:
        """Delete the Status object from the database and remove it from cache.

        :returns: None
        """
        await internal_delete(
            self,
            request={
                "route": "user_status/$status_id",
                "status_id": self.id,
                "method": "DELETE",
            },
        )

    async def increment(self, by=1):
        self.score += by
        await self.update_score()

    async def decrement(self, by=1):
        self.score -= by
        await self.update_score()

    async def update_score(self, score: int = None) -> None:
        """
        Update the score.

        :param score: int
            The player score.
        :return: None
        """
        if not score:
            score = self.score
        await basic_call(
            request={
                "route": "user_status/$status_id",
                "status_id": self.id,
                "score": score,
                "method": "PUT",
            }
        )

    async def _remove_from_cache(self) -> None:
        """Remove the Status object from cache.

        :returns: None
        """
        _statuses.pop(self.id)

    @staticmethod
    async def insert(user_id, score=0) -> int:
        """
        Insert a new status into the database.

        :param user_id: int
            The user's ID.
        :param score: int
            The score of the player.
        :returns: int
            The Status id
        """
        callback = await internal_insert(
            request={
                "route": "user_status",
                "user_id": user_id,
                "score": score,
                "method": "POST",
            }
        )
        results = callback.response.get("results")
        if not results:
            return False
        return results["adduserstatus"]

    @staticmethod
    async def get(status_id: int, fetch=True):
        """Get a Status object.

        If the Status object does not exist in cache, it will fetch the date from the API.

        :param status_id: int
            The ID of the status to get/fetch.
        :param fetch: bool
            Whether to fetch from the API if not found in cache.
        :returns: Optional[:ref:`UserStatus`]
            The UserStatus object requested.
        """
        if not status_id:
            return None
        existing = _statuses.get(status_id)
        if not existing and fetch:
            return await UserStatus.fetch(status_id)
        return existing

    @staticmethod
    async def get_all():
        """
        Get all UserStatus objects in cache.

        :returns: dict_values[:ref:`UserStatus`]
            All UserStatus objects from cache.
        """
        return _statuses.values()

    @staticmethod
    async def fetch(status_id: int):
        """Fetch an updated UserStatus object from the API.

        .. NOTE::: UserStatus objects are added to cache on creation.

        :param status_id: int
            The status ID to fetch.
        :returns: Optional[:ref:`UserStatus`]
            The user status object requested.
        """
        return await internal_fetch(
            UserStatus,
            request={
                "route": "user_status/$status_id",
                "status_id": status_id,
                "method": "GET",
            },
        )

    @staticmethod
    async def fetch_all():
        """Fetch all statuses.

        .. NOTE::: UserStatus objects are added to cache on creation.
        """
        return await internal_fetch_all(
            obj=UserStatus, request={"route": "user_status/", "method": "GET"}
        )


_statuses: Dict[int, UserStatus] = dict()
