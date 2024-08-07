import datetime
from typing import Union, List, Optional, Dict

from IreneAPIWrapper.sections import outer
from . import (
    CallBack,
    AbstractModel,
    internal_fetch,
    internal_fetch_all,
    internal_delete,
    internal_insert,
    Difficulty,
    get_difficulty,
    basic_call,
    convert_to_timestamp,
    convert_to_common_timestring
)


class UnscrambleGame(AbstractModel):
    r"""Represents an UnscrambleGame Game.

    A UnscrambleGame object inherits from :ref:`AbstractModel`.

    Parameters
    ----------
    status_ids: List[int]
        The status IDs.
    mode_id: int
        The mode of the game.
    difficulty: :ref:`Difficulty`
        The difficulty of the game.
    start_date: Optional[datetime.datetime]
        Time the game started.
    end_date: Optional[datetime.datetime]
        Time the game ended.

    Attributes
    ----------
    status_ids: List[int]
        The status IDs.
    mode_id: int
        The mode of the game.
    difficulty: :ref:`Difficulty`
        The difficulty of the game.
    start_date: Optional[datetime.datetime]
        Time the game started.
    end_date: Optional[datetime.datetime]
        Time the game ended.
    """

    def __init__(
        self,
        game_id: int,
        status_ids: List[int],
        mode_id: int,
        difficulty: Difficulty,
        start_date,
        end_date
    ):
        super(UnscrambleGame, self).__init__(game_id)
        self.status_ids = status_ids
        self.mode_id = mode_id
        self.difficulty = difficulty
        self.start_date = start_date
        self.end_date = end_date

        if not _uss.get(self.id):
            # we need to make sure not to override the current object in cache.
            _uss[self.id] = self

    @staticmethod
    async def create(*args, **kwargs):
        """
        Create a UnscrambleGame object.

        :returns: :ref:`UnscrambleGame`
        """
        game_id = kwargs.get("gameid")
        status_ids = kwargs.get("statusids")
        mode_id = kwargs.get("modeid")
        difficulty_id = kwargs.get("difficultyid")
        difficulty = get_difficulty(difficulty_id)
        start_time = convert_to_timestamp(kwargs.get("startdate"))
        end_time = convert_to_timestamp(kwargs.get("enddate"))

        UnscrambleGame(game_id, status_ids, mode_id, difficulty, start_time, end_time)

        return _uss[game_id]

    async def update_status(self, status_ids: List[int]) -> None:
        """
        Update the status ids for the game in the database.

        :return: None
        """
        self.status_ids = status_ids
        await basic_call(
            request={
                "route": "unscramblegame/$us_id",
                "game_id": self.id,
                "status_ids": self.status_ids,
                "method": "PUT",
            }
        )

    async def delete(self) -> None:
        """
        Delete the UnscrambleGame object from the database and remove it from cache.

        :returns: None
        """
        await internal_delete(
            self,
            request={
                "route": "unscramblegame/$us_id",
                "game_id": self.id,
                "method": "DELETE",
            },
        )
        await self._remove_from_cache()

    async def _remove_from_cache(self) -> None:
        """
        Remove the UnscrambleGame object from cache.

        :returns: None
        """
        _uss.pop(self.id)

    @staticmethod
    async def insert(
        start_date: datetime.datetime,
        status_ids: List[int],
        mode_id: int,
        difficulty_id: int,
    ) -> int:
        """
        Insert a new UnscrambleGame into the database.

        :param start_date: timestamp
            The start timestamp.
        :param status_ids: List[int]
            A list of status ids
        :param mode_id: int
            The guessing game's mode.
        :param difficulty_id: int
            The difficulty of the guessing game.
        :param is_nsfw: bool
            Whether the game includes nsfw content.
        :return: int
            The guessing game ID.
        """
        start_time = convert_to_common_timestring(start_date)
        callback = await internal_insert(
            request={
                "route": "unscramblegame",
                "start_date": start_time,
                "status_ids": status_ids,
                "mode_id": mode_id,
                "difficulty_id": difficulty_id,
                "method": "POST",
            }
        )

        results = callback.response.get("results")
        if not results:
            return False

        us_id = results["addus"]
        us = await UnscrambleGame.fetch(
            us_id
        )  # have the model created and added to cache.
        return us.id

    @staticmethod
    async def get(game_id: int, fetch=True):
        """Get a UnscrambleGame object.

        If the UnscrambleGame object does not exist in cache, it will fetch the id from the API.
        :param game_id: int
            The ID of the UnscrambleGame to get/fetch.
        :param fetch: bool
            Whether to fetch from the API if not found in cache.
        :returns: Optional[:ref:`UnscrambleGame`]
            The UnscrambleGame object requested.
        """
        existing = _uss.get(game_id)
        if not existing and fetch:
            return await UnscrambleGame.fetch(game_id)
        return existing

    @staticmethod
    async def get_all():
        """
        Get all UnscrambleGame objects in cache.

        :returns: dict_values[:ref:`UnscrambleGame`]
            All UnscrambleGame objects from cache.
        """
        return _uss.values()

    @staticmethod
    async def fetch(game_id: int):
        """Fetch an updated UnscrambleGame object from the API.

        .. NOTE:: affiliation objects are added to cache on creation.

        :param game_id: int
            The UnscrambleGame's ID to fetch.
        :returns: Optional[:ref:`UnscrambleGame`]
            The UnscrambleGame object requested.
        """
        return await internal_fetch(
            obj=UnscrambleGame,
            request={
                "route": "unscramblegame/$us_id",
                "game_id": game_id,
                "method": "GET",
            },
        )

    async def update_end_date(self, end_time: datetime.datetime):
        """
        Update the end time of the unscramble game.

        :param end_time: datetime.datetime
            Timestamp
        """
        end_timestring = convert_to_common_timestring(end_time)
        return await basic_call(
            request={
                "route": "unscramblegame/$us_id",
                "game_id": self.id,
                "end_time": end_timestring,
                "method": "POST",
            },
        )

    @staticmethod
    async def fetch_all():
        """Fetch all UnscrambleGame objects.

        .. NOTE:: UnscrambleGame objects are added to cache on creation.
        """
        return await internal_fetch_all(
            obj=UnscrambleGame, request={"route": "unscramblegame", "method": "GET"}
        )


_uss: Dict[int, UnscrambleGame] = dict()
