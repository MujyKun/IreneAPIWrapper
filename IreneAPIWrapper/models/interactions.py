from typing import Union, List, Optional, Dict, TYPE_CHECKING

from IreneAPIWrapper.sections import outer
from . import (
    CallBack,
    Access,
    AbstractModel,
    internal_fetch,
    internal_fetch_all,
    internal_delete,
    internal_insert,
)


class InteractionType(AbstractModel):
    r"""Represents an InteractionType object.

    An InteractionType object inherits from :ref:`AbstractModel`.

    Parameters
    ----------
    type_id: int
        Type ID
    name: str
        Name of the interaction type.

    Attributes
    ----------
    id: int
        Type ID
    name: str
        Name of the interaction type.
    """

    def __init__(self, type_id, name):
        super(InteractionType, self).__init__(type_id)
        self.name = name
        if not _interaction_types.get(self.id):
            _interaction_types[self.id] = self

    @staticmethod
    async def get(
        type_id: int,
    ):  # signature does not match on purpose; no fetching here.
        """Get an InteractionType object.

        If the InteractionType object does not exist in cache
        :param type_id: int
            The ID of the InteractionType
        :returns: Optional[:ref:`InteractionType`]
        """
        return _interaction_types.get(type_id)

    @staticmethod
    async def get_all():
        """
        Get all Interaction Type objects in cache.

        :returns: dict_values[:ref:`InteractionType`]
            All Interaction Type objects from cache.
        """
        return _interaction_types.values()

    async def delete(self) -> None:
        """
        Delete the InteractionType object from the database and remove it from cache.

        :returns: None
        """
        await internal_delete(
            self,
            request={
                "route": "interactions/type",
                "type_id": self.id,
                "method": "DELETE",
            },
        )
        await self._remove_from_cache()

    async def _remove_from_cache(self) -> None:
        """
        Remove the InteractionType object from cache.

        :returns: None
        """
        _interaction_types.pop(self.id)

    @staticmethod
    async def insert(name: str) -> None:
        """
        Insert a new interaction type into the database.

        :param name: str
            The type name.
        :return: None
        """
        name = name.lower()
        callback = await internal_insert(
            request={
                "route": "interactions/type",
                "name": name,
                "method": "POST",
            }
        )

        results = callback.response.get("results")
        if results:
            type_id = results["0"]["addinteractiontype"]
            InteractionType(type_id, name)  # add to cache.


class Interaction(AbstractModel):
    r"""Represents an Interaction object.

    An Interaction object inherits from :ref:`AbstractModel`.

    Parameters
    ----------
    interaction_type: :ref:`InteractionType`
        InteractionType
    url: str
        Interaction URL.

    Attributes
    ----------
    id: str
        InteractionType ID - URL
    type: :ref:`InteractionType`
        InteractionType
    url: str
        Interaction URL.
    """

    def __init__(self, interaction_type: InteractionType, url: str):
        super(Interaction, self).__init__(self.generate_id(interaction_type, url))
        self.type = interaction_type
        self.url: str = url
        if not _interactions.get(self.id):
            _interactions[self.id] = self

    @staticmethod
    def generate_id(interaction_type, url):
        return f"{interaction_type.id} - {url}"

    @staticmethod
    async def create(*args, **kwargs):
        """
        Create an Interaction object.

        :return: Optional[:ref:`Interaction`]
        """
        type_id = kwargs.get("typeid")
        type_name = kwargs.get("name")
        url = kwargs.get("url")

        interaction_type = await InteractionType.get(type_id)
        if not interaction_type:
            interaction_type = InteractionType(type_id, type_name)

        Interaction(interaction_type=interaction_type, url=url)
        return _interactions[Interaction.generate_id(interaction_type, url)]

    async def delete(self) -> None:
        """
        Delete the Interaction object from the database and remove it from cache.

        :returns: None
        """
        await internal_delete(
            self,
            request={
                "route": "interactions/",
                "type_id": self.type.id,
                "url": self.url,
                "method": "DELETE",
            },
        )
        await self._remove_from_cache()

    async def _remove_from_cache(self) -> None:
        """
        Remove the Interaction object from cache.

        :returns: None
        """
        _interactions.pop(self.id)

    @staticmethod
    async def insert(type_id: int, url: str) -> None:
        """
        Insert a new interaction into the database.

        :param type_id: int
            The Interaction Type.
        :param url: str
            The interaction url.
        :return: None
        """
        await internal_insert(
            request={
                "route": "interactions/",
                "type_id": type_id,
                "url": url,
                "method": "POST",
            }
        )

    @staticmethod
    async def get_all():
        """
        Get all Interaction objects in cache.

        :returns: dict_values[:ref:`Interaction`]
            All Interaction objects from cache.
        """
        return _interactions.values()

    @staticmethod
    async def fetch_all():
        """Fetch all Interactions.

        .. NOTE::: Interaction objects are added to cache on creation.
        """
        return await internal_fetch_all(
            obj=Interaction, request={"route": "interactions/", "method": "GET"}
        )


_interactions: Dict[str, Interaction] = dict()
_interaction_types: Dict[int, InteractionType] = dict()
