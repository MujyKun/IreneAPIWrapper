from typing import Optional, Dict, List
from IreneAPIWrapper.sections import outer
from . import Channel, CallBack


class Subscription:
    def __init__(self, account_name: str, followed: Optional[List[Channel]] = None):
        """
        Abstract Class for a service's account being followed by a user, guild, or channel.
        """
        self.id: str = account_name.lower()
        self._followed: List[Channel] = followed or []
        self._mention_roles: Dict[int, int] = {}  # channel_id: role_id
        self._route = None

    def __iter__(self):
        return self._followed.__iter__()

    async def add(self, channel: Channel, role_id: int = None):
        # call to api
        callback = CallBack(request={
            'route': self._route,
            'channel_id': channel.id,
            'subscription_id': self.id,
            'role_id': role_id,
            'method': 'POST',
        })
        await outer.client.add_and_wait(callback)

        self._followed.append(channel)
        if role_id:
            self._mention_roles[channel.id] = role_id

    async def remove(self, channel: Channel):
        # call to api
        callback = CallBack(request={
            'route': self._route,
            'channel_id': channel.id,
            'subscription_id': self.id,
            'method': 'DELETE',
        })

        if channel in self._followed:
            self._followed.remove(channel)

        if self._mention_roles.get(channel.id):
            self._mention_roles.pop(channel.id)
