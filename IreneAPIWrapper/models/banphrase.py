from typing import Dict

from . import (
    AbstractModel,
    internal_fetch,
    internal_fetch_all,
    internal_delete,
    internal_insert,
)


class BanPhrase(AbstractModel):
    r"""Represents a Ban Phrase.

    A Ban phrase object inherits from :ref:`AbstractModel`.

    Parameters
    ----------
    phrase_id: int
        The phrase ID.
    guild_id: int
        Guild ID.
    phrase: str
        The phrase that is banned.
    punishment: str
        Punishment of a user using the phrase.
    log_channel_id: int
        Channel ID to post the logs.


    Attributes
    ----------
    id: int
        The phrase ID.
    guild_id: int
        Guild ID.
    phrase: str
        The phrase that is banned.
    punishment: str
        Punishment of a user using the phrase.
    log_channel_id: int
        Channel ID to post the logs.
    """

    def __init__(
        self,
        phrase_id,
        guild_id,
        phrase,
        punishment,
        log_channel_id
    ):
        super(BanPhrase, self).__init__(phrase_id)
        self.guild_id: int = guild_id
        self.phrase: str = phrase
        self.punishment: str = punishment
        self.log_channel_id: int = log_channel_id

        if not _ban_phrases.get(self.id):
            _ban_phrases[self.id] = self

    @staticmethod
    async def create(*args, **kwargs):
        """Create a BanPhrase object."""
        phrase_id = kwargs.get("phraseid")
        guild_id = kwargs.get("guildid")
        punishment = kwargs.get("punishment")
        phrase = kwargs.get("phrase")
        log_channel_id = kwargs.get("logchannelid")

        BanPhrase(phrase_id=phrase_id, guild_id=guild_id, phrase=phrase, punishment=punishment,
                  log_channel_id=log_channel_id)
        return _ban_phrases[phrase_id]

    def __str__(self):
        return str(self.phrase)

    async def delete(self) -> None:
        """
        Delete the BanPhrase object from the database and remove it from cache.

        :returns: None
        """
        await internal_delete(
            self,
            request={
                "route": "banphrases/$phrase_id",
                "phrase_id": self.id,
                "method": "DELETE",
            },
        )
        await self._remove_from_cache()

    async def _remove_from_cache(self) -> None:
        """
        Remove the BanPhrase object from cache.

        :returns: None
        """
        _ban_phrases.pop(self.id)

    @staticmethod
    async def insert(
        guild_id,
        phrase,
        punishment,
        log_channel_id
    ) -> None:
        r"""
        Insert a new BanPhrase into the database and cache.

        Parameters
        ----------
        guild_id: int
            Guild ID.
        phrase: str
            Phrase to check for
        punishment: str
            Punishment for saying the phrase.
        log_channel_id: int
            Channel to send log messages to

        :returns: None
        """
        callback = await internal_insert(
            request={
                "route": "banphrases",
                "guild_id": guild_id,
                "phrase": phrase,
                "punishment": punishment,
                "log_channel_id": log_channel_id,
                "method": "POST",
            }
        )

    @staticmethod
    async def get(phrase_id: int, fetch=True):
        """Get a BanPhrase object.

        If the BanPhrase object does not exist in cache, it will fetch the person from the API.
        :param phrase_id: int
            The ID of the BanPhrase to get/fetch.
        :param fetch: bool
            Whether to fetch from the API if not found in cache.
        :returns: :ref:`BanPhrase`
        """
        existing = _ban_phrases.get(phrase_id)
        if not existing and fetch:
            return await BanPhrase.fetch(phrase_id)
        return existing

    @staticmethod
    async def get_all(guild_id=None):
        """
        Get BanPhrase objects in cache (can be filtered).

        :param guild_id: int
            Guild ID to filter by
        :returns: dict_values[:ref:`BanPhrase`]
            All BanPhrase objects from cache.
        """
        if guild_id:
            return [
                ban_phrase
                for ban_phrase in _ban_phrases.values()
                if guild_id == ban_phrase.guild_id
            ]
        return _ban_phrases.values()

    @staticmethod
    async def fetch(phrase_id: int):
        """Fetch an updated phrase object from the API.

        .. NOTE::: BanPhrase objects are added to cache on creation.

        :param phrase_id: int
            The phrase's ID to fetch.
        :returns: :ref:`BanPhrase`
        """
        return await internal_fetch(
            obj=BanPhrase,
            request={
                "route": "banphrases/$phrase_id",
                "phrase_id": phrase_id,
                "method": "GET",
            },
        )

    @staticmethod
    async def fetch_all():
        """Fetch all Ban Phrases.

        .. NOTE::: Ban phrase objects are added to cache on creation.
        """
        return await internal_fetch_all(
            obj=BanPhrase, request={"route": "banphrases/", "method": "GET"}
        )


_ban_phrases: Dict[int, BanPhrase] = dict()
