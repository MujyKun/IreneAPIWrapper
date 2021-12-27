from src.sections import outer
from . import CallBack


class BaseUser: ...  # used for type hints


_users = dict()


class User(BaseUser):
    def __init__(self, user_id: int):
        self.id = user_id
        _users[self.id] = self
        ...

    async def set_patron(self, active=True):
        callback = CallBack()
        callback.request = {
            'route': 'user/patron_status',
            'user_id': self.id,
            'method': 'POST',
            'callback_id': callback.id
        }
        await outer.client.add_to_queue(callback)
        await callback.wait_for_completion()
        # return User(**callback.response)
        ...

    async def set_super_patron(self, active=True):
        ...

    async def set_mod(self, active=True):
        ...

    async def set_data_mod(self, active=True):
        ...

    async def set_proofreader(self, active=True):
        ...

    async def set_translator(self, active=True):
        ...

    @staticmethod
    async def get(user_id: int) -> BaseUser:
        """Get a User object.

        If the User object does not exist in cache, it will fetch the user from the API.
        :param user_id: (int) The ID of the user to get/fetch.
        """
        existing_user = _users.get(user_id)
        if not existing_user:
            return await User.fetch(user_id)

    @staticmethod
    async def fetch(user_id: int) -> BaseUser:
        """Fetch an updated User object from the API."""
        callback = CallBack()
        callback.request = {
            'route': 'fetch_user',
            'user_id': user_id,
            'callback_id': callback.id
        }
        await outer.client.add_to_queue(callback)
        await callback.wait_for_completion()
        return User(**callback.response)
