from typing import Dict

from . import (
    AbstractModel,
    internal_fetch,
    internal_fetch_all,
    internal_delete,
    internal_insert,
)


class Notification(AbstractModel):
    r"""Represents a Notification.

    A Notification object inherits from :ref:`AbstractModel`.

    Note:
        One Notification object will be referenced as "noti" and not "notification".
        Several notifications will be referenced as "notifications" and not "notis"

    Parameters
    ----------
    noti_id: int
        The noti's ID.
    guild_id: int
        Guild ID of the noti.
    user_id: int
        User ID to notify.
    phrase: str
        The phrase to notify the user for.


    Attributes
    ----------
    id: int
        The noti's ID.
    guild_id: int
        Guild ID of the noti.
    user_id: int
        User ID to notify.
    phrase: str
        The phrase to notify the user for.
    """

    def __init__(
        self,
        noti_id,
        guild_id,
        user_id,
        phrase,
    ):
        super(Notification, self).__init__(noti_id)
        self.guild_id: int = guild_id
        self.user_id: int = user_id
        self.phrase: str = phrase

        if not _notifications.get(self.id):
            _notifications[self.id] = self

    @staticmethod
    async def create(*args, **kwargs):
        """Create a Noti object."""
        noti_id = kwargs.get("notiid")

        guild_id = kwargs.get("guildid")
        user_id = kwargs.get("userid")
        phrase = kwargs.get("phrase")

        Notification(noti_id=noti_id, guild_id=guild_id, user_id=user_id, phrase=phrase)
        return _notifications[noti_id]

    def __str__(self):
        return str(self.phrase)

    async def delete(self) -> None:
        """
        Delete the Noti object from the database and remove it from cache.

        :returns: None
        """
        await internal_delete(
            self,
            request={
                "route": "noti/$noti_id",
                "noti_id": self.id,
                "method": "DELETE",
            },
        )
        await self._remove_from_cache()

    async def _remove_from_cache(self) -> None:
        """
        Remove the Noti object from cache.

        :returns: None
        """
        _notifications.pop(self.id)

    @staticmethod
    async def insert(
        guild_id,
        user_id,
        phrase,
    ) -> None:
        r"""
        Insert a new Noti into the database and cache.

        Parameters
        ----------
        guild_id: int
            Guild ID.
        user_id: int
            User ID to be notified.
        phrase: str
            Phrase to notify the user for.

        :returns: None
        """
        callback = await internal_insert(
            request={
                "route": "noti",
                "guild_id": guild_id,
                "user_id": user_id,
                "phrase": phrase,
                "method": "POST",
            }
        )
        results = callback.response.get("results")
        if not results:
            return False

        noti_id = results["addnotification"]
        await Notification.fetch(noti_id)  # add object to cache.
        return noti_id

    @staticmethod
    async def get(noti_id: int, fetch=True):
        """Get a Noti object.

        If the Noti object does not exist in cache, it will fetch the person from the API.
        :param noti_id: int
            The ID of the Noti to get/fetch.
        :param fetch: bool
            Whether to fetch from the API if not found in cache.
        :returns: :ref:`Notification`
        """
        existing = _notifications.get(noti_id)
        if not existing and fetch:
            return await Notification.fetch(noti_id)
        return existing

    @staticmethod
    async def get_all(guild_id=None, user_id=None):
        """
        Get Notification objects in cache (can be filtered).

        :param guild_id: int
            Guild ID to filter by
        :param user_id: int
            User ID to filter by
        :returns: dict_values[:ref:`Notification`]
            All Notification objects from cache.
        """
        if guild_id and user_id:
            return [
                noti
                for noti in _notifications.values()
                if guild_id == noti.guild_id and user_id == noti.user_id
            ]
        elif guild_id:
            return [
                noti for noti in _notifications.values() if guild_id == noti.guild_id
            ]
        elif user_id:
            return [noti for noti in _notifications.values() if user_id == noti.user_id]
        return _notifications.values()

    @staticmethod
    async def fetch(noti_id: int):
        """Fetch an updated noti object from the API.

        .. NOTE::: Noti objects are added to cache on creation.

        :param noti_id: int
            The noti's ID to fetch.
        :returns: :ref:`Notification`
        """
        return await internal_fetch(
            obj=Notification,
            request={
                "route": "noti/$noti_id",
                "noti_id": noti_id,
                "method": "GET",
            },
        )

    @staticmethod
    async def fetch_all():
        """Fetch all Notifications.

        .. NOTE::: Notification objects are added to cache on creation.
        """
        return await internal_fetch_all(
            obj=Notification, request={"route": "noti/", "method": "GET"}
        )


_notifications: Dict[int, Notification] = dict()
