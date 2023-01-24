from typing import Union, List, Optional, Dict

from . import (
    AbstractModel,
    internal_fetch,
    internal_fetch_all,
    internal_delete,
    internal_insert,
)


class ReactionRoleMessage(AbstractModel):
    r"""Represents a reaction role message.

    A ReactionRoleMessage object inherits from :ref:`AbstractModel`.

    Parameters
    ----------
    message_id: int
        The message id.
    """
    def __init__(
            self,
            message_id: int
    ):
        super(ReactionRoleMessage, self).__init__(message_id)
        if not _reaction_messages.get(self.id):
            # we need to make sure not to override the current object in cache.
            _reaction_messages[self.id] = self

    @staticmethod
    def priority():
        return 0

    @staticmethod
    async def create(*args, **kwargs):
        """
        Create an ReactionRoleMessage object.

        :returns: :ref:`ReactionRoleMessage`
        """
        message_id = kwargs.get("messageid")
        ReactionRoleMessage(message_id)
        return _reaction_messages[message_id]

    @staticmethod
    async def insert(message_id: int):
        """
        Insert a new message into the database.

        :param message_id: int
            The message ID.
        """
        callback = await internal_insert(
            request={
                "route": "reaction_roles/$message_id",
                "message_id": message_id,
                "method": "POST",
            }
        )
        # insert into cache.
        await ReactionRoleMessage.create(**{"messageid": message_id})
        return True

    @staticmethod
    async def get_all():
        """
        Get all ReactionRoleMessage objects in cache.

        :returns: dict_values[:ref:`ReactionRoleMessage`]
            All ReactionRoleMessage objects from cache.
        """
        return _reaction_messages.values()

    @staticmethod
    async def fetch_all():
        """Fetch all ReactionRoleMessage.

        .. NOTE:: ReactionRoleMessage objects are added to cache on creation.
        """
        return await internal_fetch_all(
            obj=ReactionRoleMessage, request={"route": "reaction_roles/", "method": "GET"}
        )


_reaction_messages: Dict[int, ReactionRoleMessage] = dict()
