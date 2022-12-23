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
    Date
)


class Reminder(AbstractModel):
    r"""Represents a user needing to be notified for a reason at a specific time.

    A Reminder object inherits from :ref:`AbstractModel`.

    Parameters
    ----------
    reminder_id: int
        The reminder ID
    user_id: int
        The user ID to notify.
    reason: str,
        The reason for being reminded.
    date: :ref:`Date`
        The date object containing when the user should be reminded.

    Attributes
    ----------
    user_id: int
        The user ID to notify.
    reason: str,
        The reason for being reminded.
    date: :ref:`Date`
        The date object containing when the user should be reminded.
    """

    def __init__(self, reminder_id, user_id: int, reason: str, date: Date):
        super(Reminder, self).__init__(reminder_id)
        self.user_id: int = user_id
        self.reason: str = reason
        self.date: Date = date

        if not _reminders.get(self.id):
            _reminders[self.id] = self

    @staticmethod
    async def create(*args, **kwargs):
        """
        Create a Reminder object.

        :returns: :ref:`Reminder`
        """
        remind_id = kwargs.get("remindid")
        user_id = kwargs.get("userid")
        reason = kwargs.get("reason")
        date_id = kwargs.get("dateid")
        date = await Date.get(date_id)

        Reminder(remind_id, user_id, reason, date)
        return _reminders[remind_id]

    async def delete(self) -> None:
        """Delete the Reminder object from the database and remove it from cache.

        :returns: None
        """
        await internal_delete(
            self,
            request={"route": "reminder/$remind_id", "remind_id": self.id, "method": "DELETE"},
        )
        await self._remove_from_cache()

    async def _remove_from_cache(self) -> None:
        """Remove the Date object from cache.

        :returns: None
        """
        _reminders.pop(self.id)

    @staticmethod
    async def insert(user_id, reason, date: Date) -> int:
        """
        Insert a new reminder into the database.

        :param user_id: int
            The User ID to remind.
        :param reason: str
            The reason to remind the user.
        :param date: :ref:`Date`
            The date object containing when the user should be reminded.
        :returns: int
            The reminder id
        """
        callback = await internal_insert(
            request={
                "route": "reminder",
                "user_id": user_id,
                "reason": reason or "Do Nothing",
                "date_id": date.id,
                "method": "POST",
            }
        )

        results = callback.response.get("results")
        if not results:
            return False

        return results["addreminder"]

    @staticmethod
    async def get(remind_id: int, fetch=True):
        """Get a Reminder object.

        If the Reminder object does not exist in cache, it will fetch the reminder from the API.

        :param remind_id: int
            The ID of the reminder to get/fetch.
        :param fetch: bool
            Whether to fetch from the API if not found in cache.
        :returns: Optional[:ref:`Reminder`]
            The reminder object requested.
        """
        if not remind_id:
            return None
        existing = _reminders.get(remind_id)
        if not existing and fetch:
            return await Date.fetch(remind_id)
        return existing

    @staticmethod
    async def get_all():
        """
        Get all Reminder objects in cache.

        :returns: dict_values[:ref:`Reminder`]
            All Reminder objects from cache.
        """
        return _reminders.values()

    @staticmethod
    async def fetch(remind_id: int):
        """Fetch an updated Reminder object from the API.

        .. NOTE::: Reminder objects are added to cache on creation.

        :param remind_id: int
            The reminder's ID to fetch.
        :returns: Optional[:ref:`Reminder`]
            The reminder object requested.
        """
        return await internal_fetch(
            Reminder,
            request={"route": "reminder/$remind_id", "remind_id": remind_id, "method": "GET"},
        )

    @staticmethod
    async def fetch_all():
        """Fetch all reminders.

        .. NOTE::: Reminders objects are added to cache on creation.
        """
        return await internal_fetch_all(
            obj=Reminder, request={"route": "reminder/", "method": "GET"}
        )


_reminders: Dict[int, Reminder] = dict()
