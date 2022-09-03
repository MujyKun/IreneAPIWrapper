from typing import Optional, Dict, List, Union
from IreneAPIWrapper.sections import outer
from . import Channel, CallBack, AbstractModel


class Subscription(AbstractModel):
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
    """

    def __init__(
        self,
        account_id: Union[int, str],
        account_name: str,
        followed: Optional[List[Channel]] = None,
        mention_roles: Optional[Dict[Channel, int]] = None,
    ):
        super(Subscription, self).__init__(account_id)
        self.name: str = account_name.lower()
        self._followed: List[Channel] = followed or []
        self._mention_roles: Dict[Channel, int] = mention_roles or {}

    def __iter__(self):
        return self._followed.__iter__()

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id

    def _sub_in_cache(
        self,
        channel: Channel = None,
        role_id: int = None,
        channels: Optional[List[Channel]] = None,
        role_ids: Optional[Dict[Channel, int]] = None,
    ):
        """
        Make a channel subscribe.

        :param channel: Union[:ref:`Channel`, List[:ref:`Channel`]
            A :ref:`Channel` object to add to cache.
        :param role_id: int
            The role ID to add.
        """
        if channel and channel not in self:
            self._followed.append(channel)

        if role_id and channel:
            self._mention_roles[channel] = role_id

        if channels:
            self._followed += [
                _channel for _channel in channels if _channel not in self._followed
            ]

        if role_ids:
            self._mention_roles |= role_ids  # merge the dictionaries.

    def _unsub_in_cache(self, channel: Channel):
        """
        Make a channel unsubscribe.

        :param channel: :ref:`Channel`
            A :ref:`Channel` object to remove from cache.
        """
        if channel in self._followed:
            self._followed.remove(channel)

        if self._mention_roles.get(channel):
            self._mention_roles.pop(channel)

    async def unsubscribe(self, channel: Channel) -> None:
        """
        Unsubscribe from an account.
        :param channel: :ref:`Channel`
        :return: None
        """

    async def subscribe(self, channel: Channel, role_id: Optional[int] = None) -> None:
        """
        Subscribe to a channel.
        :param role_id: The role id to notify.
        :param channel: :ref:`Channel`
        :return: None
        """

    async def get_role_id(self, channel: Channel):
        """Get the role id to mention of a channel."""
        return self._mention_roles.get(channel)

    def check_subscribed(self, channels: List[Channel]) -> List[Channel]:
        """Checks which :ref:`Channel`s are subscribed to the current subscription account
        from a selection of channels.

        :param channels: List[:ref:`Channel`]
        :returns List[:ref:`Channel`]
            A list of :ref:`Channel`s from the channels provided that are subscribed.
        """
        return [channel for channel in channels if channel in self]
