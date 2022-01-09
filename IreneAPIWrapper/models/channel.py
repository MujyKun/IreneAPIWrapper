from typing import Dict
from . import CallBack
from IreneAPIWrapper.sections import outer


class Channel:
    def __init__(self, channel_id):
        self.id = channel_id

    def __eq__(self, other):
        return self.id == other.id

    def __ne__(self, other):
        return self.id != other.id

    @staticmethod
    async def get(channel_id):
        """
        Get a channel object.

        Will attempt to insert if it is not already existing in cache, then add it to cache.
        :param channel_id: The channel ID to retrieve.
        :return: (Channel) The channel object requested.
        """
        channel = _channels.get(channel_id)
        if channel:
            return channel

        if not channel:
            channel = Channel(channel_id)
            await Channel._add(channel_id)
            _channels[channel_id] = channel
        return channel

    @staticmethod
    async def _add(channel_id):
        """
        Add the channel ID to the Database.

        The API will deal with already existing channels.
        Does not add to cache.
        :param channel_id: The channel ID to add.
        """

        callback = CallBack(request={
            'route': 'channel/$channel_id',
            'channel_id': channel_id,
            'method': 'POST'}
        )
        await outer.client.add_and_wait(callback)

    async def _delete(self):
        """
        Delete the channel from the Database.

        This is a permanent change and cascades all existing objects that are dependent on the channel.
        Will remove the object from cache.
        """

        callback = CallBack(request={
            'route': 'channel/$channel_id',
            'channel_id': self.id,
            'method': 'DELETE'}
        )
        outer.client.add_and_wait(callback)
        _channels.pop(self.id)


_channels: Dict[int, Channel] = dict()
