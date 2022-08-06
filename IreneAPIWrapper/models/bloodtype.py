from typing import Union, List, Optional, Dict

from IreneAPIWrapper.sections import outer
from . import (
    CallBack,
    Access,
    AbstractModel,
    internal_fetch,
    internal_fetch_all,
    MediaSource,
)


class BloodType(AbstractModel):
    r"""Represents a BloodType.

    A BloodType object inherits from :ref:`AbstractModel`.

    Please note that the blood types are metadata.
    While it may be possible to delete/remove blood types from the API, it will not be possible in this wrapper
    to avoid unnecessary changes.

    .. Note:: Possible Blood Types:
        O-
        O+
        A-
        A+
        B-
        B+
        AB-
        AB+

    Attributes
    ----------
    id: int
        The blood type's id.
    name: str
        The name of the blood type.
    """

    def __init__(self, blood_id, name):
        super(BloodType, self).__init__(blood_id)
        self.name = name

        if not _blood_types.get(self.id):
            _blood_types[self.id] = self

    @staticmethod
    async def create(*args, **kwargs):
        blood_id = kwargs.get("bloodid")
        name = kwargs.get("name")

        BloodType(blood_id, name)
        return _blood_types[blood_id]

    async def _remove_from_cache(self):
        """Remove the blood type from cache."""
        _blood_types.pop(self.id)

    @staticmethod
    async def get(blood_id: int, fetch=True):
        """Get a BloodType object.

        If the BloodType object does not exist in cache, it will fetch the name from the API.

        :param blood_id: int
            The ID of the blood type to get/fetch.
        :param fetch: bool
            Whether to fetch from the API if not found in cache.
        :returns: Optional[:ref:`BloodType`]
            The blood type object requested.
        """
        existing = _blood_types.get(blood_id)
        if not existing and fetch:
            return await BloodType.fetch(blood_id)
        return existing

    @staticmethod
    async def get_all():
        """
        Get all BloodType objects in cache.

        :returns: dict_values[:ref:`BloodType`]
            All BloodType objects from cache.
        """
        return _blood_types.values()

    @staticmethod
    async def fetch(blood_id: int):
        """Fetch an updated BloodType object from the API.

        .. NOTE:: BloodType objects are added to cache on creation.

        :param blood_id: int
            The blood's ID to fetch.
        :returns: Optional[:ref:`BloodType`]
            The blood type object requested.
        """
        if not blood_id:
            return None

        return await internal_fetch(
            obj=BloodType,
            request={
                "route": "bloodtype/$blood_id",
                "blood_id": blood_id,
                "method": "GET",
            },
        )

    @staticmethod
    async def fetch_all():
        """Fetch all blood types.

        .. NOTE:: BloodType objects are added to cache on creation.
        """
        return await internal_fetch_all(
            obj=BloodType, request={"route": "bloodtype/", "method": "GET"}
        )


_blood_types: Dict[int, BloodType] = dict()
