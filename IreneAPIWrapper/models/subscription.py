from typing import Optional, Dict, List
from IreneAPIWrapper.sections import outer
from . import Channel, CallBack


class Subscription:
    def __init__(self, account_id: int, account_name: str, followed: Optional[List[Channel]] = None):
        """
        Abstract Class for a service's account being followed by a user, guild, or channel.
        """
        self.id: int = account_id
        self.name: str = account_name.lower()
        self._followed: List[Channel] = followed or []
        self._mention_roles: Dict[Channel, int] = {}  # channel_id: role_id
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

        :param channel: (Channel) A Channel object to add to cache.
        :param role_id: (int) The role ID to add.
        """
        self._followed.append(channel)
        if role_id:
            self._mention_roles[channel] = role_id

    def _remove_from_cache(self, channel: Channel):
        """
        Make a channel unsubscribe from the cache.

        :param channel: (Channel) A Channel object to remove from cache.
        """
        if channel in self._followed:
            self._followed.remove(channel)

        if self._mention_roles.get(channel):
            self._mention_roles.pop(channel)

