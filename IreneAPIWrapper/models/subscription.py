from typing import Optional, Dict, List
from IreneAPIWrapper.sections import outer
from . import Channel, CallBack


class Subscription:
    r"""
    Abstract Subscription Class for a service account being followed by a user, guild, or channel.

    .. container:: operations
        .. describe:: x == y
            Checks if two service accounts have the same ID.
        .. describe:: x != y
            Checks if two service accounts do not have the same ID.

    Parameters
    ----------
    account_id: int
        The account's ID.
    account_name: str
        The account's name.
    followed: Optional[List[:ref:`Channel`]]
        The :ref:`Channel` objects following the service account.

    Attributes
    ----------
    id: int
        Account ID.
    name: str
        The account's name.
    _followed: List[:ref:`Channel`]
        The list of :ref:`Channel` objects followed to the service account.
    _mention_roles: Dict[:ref:`Channel`, int]
        :ref:`Channel` objects associated with role ids to mention on updates.
    _route: Unknown
        Unknown what this attribute is used for. Will find out eventually.
        May have been in the early stages of the API where REST routes were planned to be used instead of a Websocket.

    """
    def __init__(self, account_id: int, account_name: str, followed: Optional[List[Channel]] = None):

        self.id: int = account_id
        self.name: str = account_name.lower()
        self._followed: List[Channel] = followed or []
        self._mention_roles: Dict[Channel, int] = {}  # channel_id: role_id

        # TODO: figure out what self._route was made for.
        self._route = None

    def __iter__(self):
        return self._followed.__iter__()

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id

    def _add_to_cache(self, channel: Channel, role_id: int = None):
        """
        Make a channel subscribe in cache.

        :param channel: :ref:`Channel`
            A :ref:`Channel` object to add to cache.
        :param role_id: int
            The role ID to add.
        """
        self._followed.append(channel)
        if role_id:
            self._mention_roles[channel] = role_id

    def _remove_from_cache(self, channel: Channel):
        """
        Make a channel unsubscribe from the cache.

        :param channel: :ref:`Channel`
            A :ref:`Channel` object to remove from cache.
        """
        if channel in self._followed:
            self._followed.remove(channel)

        if self._mention_roles.get(channel):
            self._mention_roles.pop(channel)

