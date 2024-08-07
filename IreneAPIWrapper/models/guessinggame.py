import datetime
from typing import Union, List, Optional, Dict

from IreneAPIWrapper.sections import outer
from . import (
    CallBack,
    Access,
    AbstractModel,
    internal_fetch,
    internal_fetch_all,
    MediaSource,
    Position,
    Person,
    Group,
    internal_delete,
    internal_insert,
    Difficulty,
    get_difficulty,
    basic_call,
    convert_to_timestamp,
    convert_to_common_timestring
)


class GuessingGame(AbstractModel):
    r"""Represents a Guessing Game.

    A GuessingGame object inherits from :ref:`AbstractModel`.

    Parameters
    ----------
    media_ids: List[int]
        The media IDs.
    status_ids: List[int]
        The status IDs.
    mode_id: int
        The mode of the game.
    difficulty: :ref:`Difficulty`
        The difficulty of the game.
    is_nsfw: bool
        Whether the content may be NSFW.
    start_date: Optional[datetime.datetime]
        Time the game started.
    end_date: Optional[datetime.datetime]
        Time the game ended.

    Attributes
    ----------
    media_ids: List[int]
        The media IDs.
    status_ids: List[int]
        The status IDs.
    mode_id: int
        The mode of the game.
    difficulty: :ref:`Difficulty`
        The difficulty of the game.
    is_nsfw: bool
        Whether the content may be NSFW.
    start_date: Optional[datetime.datetime]
        Time the game started.
    end_date: Optional[datetime.datetime]
        Time the game ended.
    """

    def __init__(
        self,
        game_id: int,
        media_ids: List[int],
        status_ids: List[int],
        mode_id: int,
        difficulty: Difficulty,
        is_nsfw: bool,
        start_date,
        end_date
    ):
        super(GuessingGame, self).__init__(game_id)
        self.media_ids = media_ids
        self.status_ids = status_ids
        self.mode_id = mode_id
        self.difficulty = difficulty
        self.is_nsfw = is_nsfw
        self.start_date = start_date
        self.end_date = end_date

        if not _ggs.get(self.id):
            # we need to make sure not to override the current object in cache.
            _ggs[self.id] = self

    @staticmethod
    async def create(*args, **kwargs):
        """
        Create a GuessingGame object.

        :returns: :ref:`GuessingGame`
        """
        game_id = kwargs.get("gameid")
        media_ids = kwargs.get("mediaids")
        status_ids = kwargs.get("statusids")
        mode_id = kwargs.get("modeid")
        difficulty_id = kwargs.get("difficultyid")
        difficulty = get_difficulty(difficulty_id)
        is_nsfw = kwargs.get("isnsfw")
        start_time = convert_to_timestamp(kwargs.get("startdate"))
        end_time = convert_to_timestamp(kwargs.get("enddate"))

        GuessingGame(game_id, media_ids, status_ids, mode_id, difficulty, is_nsfw, start_time, end_time)

        return _ggs[game_id]

    async def update_media_and_status(
        self, media_ids: List[int], status_ids: List[int]
    ) -> None:
        """
        Update the media and status ids for the game in the database.

        :return: None
        """
        self.media_ids = media_ids
        self.status_ids = status_ids
        await basic_call(
            request={
                "route": "guessinggame/$gg_id",
                "game_id": self.id,
                "media_ids": self.media_ids,
                "status_ids": self.status_ids,
                "method": "PUT",
            }
        )

    async def delete(self) -> None:
        """
        Delete the GuessingGame object from the database and remove it from cache.

        :returns: None
        """
        await internal_delete(
            self,
            request={
                "route": "guessinggame/$gg_id",
                "game_id": self.id,
                "method": "DELETE",
            },
        )
        await self._remove_from_cache()

    async def _remove_from_cache(self) -> None:
        """
        Remove the GuessingGame object from cache.

        :returns: None
        """
        _ggs.pop(self.id)

    @staticmethod
    async def insert(
        start_date: datetime.datetime,
        media_ids: List[int],
        status_ids: List[int],
        mode_id: int,
        difficulty_id: int,
        is_nsfw: bool,
    ) -> int:
        """
        Insert a new GuessingGame into the database.

        :param start_date: timestamp
            The start timestamp.
        :param media_ids: List[int]
            A list of media object ids.
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
                "route": "guessinggame",
                "start_date": start_time,
                "media_ids": media_ids,
                "status_ids": status_ids,
                "mode_id": mode_id,
                "difficulty_id": difficulty_id,
                "is_nsfw": is_nsfw,
                "method": "POST",
            }
        )

        results = callback.response.get("results")
        if not results:
            return False

        gg_id = results["addgg"]
        gg = await GuessingGame.fetch(
            gg_id
        )  # have the model created and added to cache.
        return gg.id

    @staticmethod
    async def get(game_id: int, fetch=True):
        """Get a GuessingGame object.

        If the GuessingGame object does not exist in cache, it will fetch the id from the API.
        :param game_id: int
            The ID of the GuessingGame to get/fetch.
        :param fetch: bool
            Whether to fetch from the API if not found in cache.
        :returns: Optional[:ref:`GuessingGame`]
            The GuessingGame object requested.
        """
        existing = _ggs.get(game_id)
        if not existing and fetch:
            return await GuessingGame.fetch(game_id)
        return existing

    @staticmethod
    async def get_all():
        """
        Get all GuessingGame objects in cache.

        :returns: dict_values[:ref:`GuessingGame`]
            All GuessingGame objects from cache.
        """
        return _ggs.values()

    @staticmethod
    async def fetch(game_id: int):
        """Fetch an updated GuessingGame object from the API.

        .. NOTE:: affiliation objects are added to cache on creation.

        :param game_id: int
            The GuessingGame's ID to fetch.
        :returns: Optional[:ref:`GuessingGame`]
            The GuessingGame object requested.
        """
        return await internal_fetch(
            obj=GuessingGame,
            request={
                "route": "guessinggame/$gg_id",
                "game_id": game_id,
                "method": "GET",
            },
        )

    async def update_end_date(self, end_time: datetime.datetime):
        """
        Update the end time of the guessing game.

        :param end_time: datetime.datetime
            Timestamp
        """
        end_timestring = convert_to_common_timestring(end_time)
        return await basic_call(
            request={
                "route": "guessinggame/$gg_id",
                "game_id": self.id,
                "end_time": end_timestring,
                "method": "POST",
            },
        )

    @staticmethod
    async def fetch_all():
        """Fetch all GuessingGame objects.

        .. NOTE:: GuessingGame objects are added to cache on creation.
        """
        return await internal_fetch_all(
            obj=GuessingGame, request={"route": "guessinggame", "method": "GET"}
        )


_ggs: Dict[int, GuessingGame] = dict()
