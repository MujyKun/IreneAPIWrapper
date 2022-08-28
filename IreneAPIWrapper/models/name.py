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
)


class Name(AbstractModel):
    r"""Represents names for an entity that may have several types.

    A Name object inherits from :ref:`AbstractModel`.

    Parameters
    ----------
    name_id: int
        The Name id.
    first: str
        First part of the name.
    last: str
        Last part of the name.

    Attributes
    ----------
    id: int
        The Name id.
    first: str
        First part of the name.
    last: str
        Last part of the name.

    """

    def __init__(self, name_id, first, last):
        super(Name, self).__init__(name_id)
        self.id = name_id
        self.first: str = first
        self.last: str = last
        if not _names.get(self.id):
            _names[self.id] = self

    def __str__(self):
        return f"{self.first} {self.last}"

    async def get_card(self, markdown=False, extra=True):
        card_data = []
        if self.id:
            card_data.append(f"Name ID: {self.id}")
        card_data.append(f"Name: {str(self)}")
        return card_data

    @staticmethod
    async def create(*args, **kwargs):
        """
        Create a name object.

        :returns: :ref:`Name`
        """
        name_id = kwargs.get("nameid")
        first = kwargs.get("firstname")
        last = kwargs.get("lastname")

        Name(name_id, first, last)
        return _names[name_id]

    async def delete(self) -> None:
        """
        Delete the Name object from the database and remove it from cache.

        :returns: None
        """
        await internal_delete(
            self,
            request={"route": "name/$name_id", "name_id": self.id, "method": "DELETE"},
        )
        await self._remove_from_cache()

    async def _remove_from_cache(self) -> None:
        """
        Remove the Name object from cache.

        :returns: None
        """
        _names.pop(self.id)

    @staticmethod
    async def insert(first, last) -> None:
        """
        Insert a new name into the database.

        :param first: str
            The first part of the name.
        :param last: str
            The last part of the name.

        :returns: None
        """
        await internal_insert(
            request={
                "route": "name",
                "first_name": first,
                "last_name": last,
                "method": "POST",
            }
        )

    @staticmethod
    async def get(name_id: int, fetch=True):
        """Get a Name object.

        If the Name object does not exist in cache, it will fetch the name from the API.
        :param name_id: int
            The ID of the name to get/fetch.
        :param fetch: bool
            Whether to fetch from the API if not found in cache.
        :returns: :ref:`Name`
        """
        existing = _names.get(name_id)
        if not existing and fetch:
            return await Name.fetch(name_id)
        return existing

    @staticmethod
    async def get_all():
        """
        Get all Name objects in cache.

        :returns: dict_values[:ref:`Name`]
            All Name objects from cache.
        """
        return _names.values()

    @staticmethod
    async def fetch(name_id: int):
        """Fetch an updated Name object from the API.

        .. NOTE::: Name objects are added to cache on creation.

        :param name_id: int
            The name's ID to fetch.
        :returns: :ref:`Name`
        """
        return await internal_fetch(
            obj=Name,
            request={"route": "name/$name_id", "name_id": name_id, "method": "GET"},
        )

    @staticmethod
    async def fetch_all():
        """Fetch all names.

        .. NOTE::: Name objects are added to cache on creation.
        """
        return await internal_fetch_all(
            obj=Name, request={"route": "name/", "method": "GET"}
        )


_names: Dict[int, Name] = dict()
