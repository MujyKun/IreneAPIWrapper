from typing import List


class AbstractModel:
    def __init__(self, obj_id):
        r"""An abstract model to assist with type hints, the creation, and fetching of cache objects.

        .. container:: operations
            .. describe:: x == y
                Checks if two models have the same ID.
            .. describe:: x != y
                Checks if two models do not have the same ID.

        Arguments
        ---------
        id: int
            The model's id.

        Attributes
        ----------
        id: int
            The model's id.
        """
        self.id = obj_id

    @staticmethod
    def priority():
        return 0

    def __hash__(self):
        return id(self)

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id

    async def delete(self):
        """Delete the current object from the database and remove it from cache."""
        ...

    async def get_card(self, markdown=False):
        """
        Get a list representing of the current object as a card.

        :param markdown: bool
            Whether the returned list should support markdown.
        :return: List[str]
            A list of strings for the card.
        """

    async def _remove_from_cache(self):
        """Remove the current object from cache."""
        ...

    @staticmethod
    async def insert(*args, **kwargs):
        """Insert a new object into the database."""
        ...

    @staticmethod
    async def create(*args, **kwargs):
        """Create an object."""
        ...

    @staticmethod
    async def create_bulk(list_of_dicts: List[dict]):
        """Bulk create objects

        :param list_of_dicts: List[dict]
            A list of dictionaries.
        """

    @staticmethod
    async def get(unique_id: int, fetch: bool):
        """Get an object if it exists in cache, otherwise fetch the object from the API."""
        ...

    @staticmethod
    async def fetch(unique_id: int):
        """Fetch the object from the API."""
        ...

    @staticmethod
    async def fetch_all():
        """Fetch all objects from the API."""
        ...
