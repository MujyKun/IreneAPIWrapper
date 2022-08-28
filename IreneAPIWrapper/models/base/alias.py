from typing import Optional

from . import AbstractModel


class Alias(AbstractModel):
    r"""Represents an Abstract Alias.

    An Alias object inherits from :ref:`AbstractModel`.

    Please note that concrete aliases of different types will overlap unique keys,
    so they must have their own cache per concrete type of alias.

    Parameters
    ----------
    alias_id: int
        The Alias id.
    alias_name: str
        The alias name.
    obj_id: int
        The ID of the object the alias is referring to.
    guild_id: Optional[int]
        A guild ID that owns the alias if there is one.

    Attributes
    ----------
    id: int
        The Alias id.
    name: str
        The alias name.
    _obj_id: int
        The ID of the object the alias is referring to. Used for Abstraction.
    guild_id: Optional[int]
         A guild ID that owns the alias if there is one.
    """

    def __init__(self, alias_id, alias_name, obj_id, guild_id):
        super(Alias, self).__init__(alias_id)
        self.name: str = alias_name
        self._obj_id: int = obj_id
        self.guild_id: Optional[int] = guild_id

    def __str__(self):
        return self.name
