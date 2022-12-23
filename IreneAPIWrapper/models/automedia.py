from typing import Union, List, Optional, Dict

from . import (
    AbstractModel,
    internal_fetch,
    internal_fetch_all,
    internal_delete,
    internal_insert,
)
from dataclasses import dataclass


@dataclass
class AffiliationTime:
    r"""Holds an affiliation ID and the number of hours before it gets posted."""
    affiliation_id: int
    hours_after: int


class AutoMedia(AbstractModel):
    r"""Represents automatically sending media.

    An AutoMedia object inherits from :ref:`AbstractModel`.

    Parameters
    ----------
    channel_id: int
        The text channel id.
    aff_times: List[:ref:`AffiliationTime`]
        The Affiliation Times.

    Attributes
    ----------
    channel_id: int
        The Channel id.
    aff_times: List[:ref:`AffiliationTime`]
        The Affiliation Times.
    """

    def __init__(
            self,
            channel_id: int,
            aff_times: List[AffiliationTime],
    ):
        super(AutoMedia, self).__init__(channel_id)
        self.aff_times: List[AffiliationTime] = aff_times

        if not _automedias.get(self.id):
            # we need to make sure not to override the current object in cache.
            _automedias[self.id] = self

    @staticmethod
    def priority():
        return 0

    @staticmethod
    async def create(*args, **kwargs):
        """
        Create an AutoMedia object.

        :returns: :ref:`AutoMedia`
        """
        channel_id = kwargs.get("channelid")
        affiliation_id = kwargs.get("affiliationid")
        hours_after = kwargs.get("hoursafter")

        aff_time = AffiliationTime(affiliation_id, hours_after)

        existing_obj = _automedias.get(channel_id)
        if existing_obj:
            await existing_obj.add_to_cache(aff_time)
        else:
            AutoMedia(channel_id, [aff_time])

        return _automedias[channel_id]

    async def add_to_cache(self, aff_time: AffiliationTime):
        """
        Add an affiliation time to cache.

        :param aff_time: :ref:`AffiliationTime`
            The affiliation time to add to cache.
        """
        if aff_time not in self.aff_times:
            self.aff_times.append(aff_time)

    async def remove_from_cache(self, aff_time: AffiliationTime):
        """
        Remove an affiliation time from cache.

        :param aff_time: :ref:`AffiliationTime`
            The affiliation time to remove from cache.
        """
        if aff_time in self.aff_times:
            self.aff_times.remove(aff_time)

    async def delete_aff_time(self, aff_time: AffiliationTime) -> None:
        """Delete the :ref:`AffiliationTime` object from the database and remove it from cache.

        :param aff_time: :ref:`AffiliationTime`
            The affiliation time to delete.
        """
        await internal_delete(
            self,
            request={
                "route": "affiliation/automedia",
                "channel_id": self.id,
                "affiliation_id": aff_time.affiliation_id,
                "method": "DELETE",
            },
        )
        await self.remove_from_cache(aff_time)

    @staticmethod
    async def insert(channel_id: int, affiliation_id: int, hours_after: int):
        """
        Insert a new aff time into the database.

        :param channel_id: int
            The channel ID.
        :param affiliation_id: int
            The affiliation ID
        :param hours_after: int
            Hours before each media post is sent.
        """
        callback = await internal_insert(
            request={
                "route": "affiliation/automedia",
                "channel_id": channel_id,
                "affiliation_id": affiliation_id,
                "hours_after": hours_after,
                "method": "POST",
            }
        )
        # insert into cache.
        await AutoMedia.create(**{"channelid": channel_id, "affiliationid": affiliation_id, "hoursafter": hours_after})
        return True

    @staticmethod
    async def get(channel_id: int, fetch=True):
        """Get an AutoMedia object.

        If the AutoMedia object does not exist in cache, it will fetch it from the API.
        :param channel_id: int
            Channel ID
        :param fetch: bool
            Whether to fetch from the API if not found in cache.
        :returns: Optional[:ref:`AutoMedia`]
            The AutoMedia object requested.
        """
        existing = _automedias.get(channel_id)
        if not existing and fetch:
            await AutoMedia.fetch_all()  # have all aff times added..
            existing = _automedias.get(channel_id)
        if not existing:
            existing = AutoMedia(channel_id, [])
        return existing

    @staticmethod
    async def get_all():
        """
        Get all AutoMedia objects in cache.

        :returns: dict_values[:ref:`AutoMedia`]
            All AutoMedia objects from cache.
        """
        return _automedias.values()

    @staticmethod
    async def fetch(channel_id: int):
        """Fetch an auto media from the API

        .. NOTE:: It is not currently possible to do so through the API.
        It is advised to use `get` instead which will use `fetch_all` as a reserve.

        :param channel_id: int
            The channel's ID to fetch.
        :returns: Optional[:ref:`AutoMedia`]
            The AutoMedia object requested.
        """
        raise NotImplementedError


    @staticmethod
    async def fetch_all():
        """Fetch all automedia.

        .. NOTE:: affiliation objects are added to cache on creation.
        """
        return await internal_fetch_all(
            obj=AutoMedia, request={"route": "affiliation/automedia", "method": "GET"}
        )


_automedias: Dict[int, AutoMedia] = dict()