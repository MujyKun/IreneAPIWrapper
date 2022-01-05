from typing import Union, List, Optional, Dict

from IreneAPIWrapper.sections import outer
from . import CallBack, Access


class BaseUser: ...  # used for type hints


class User(BaseUser):
    def __init__(self, user_id: int, *args, **kwargs):
        self.id: int = user_id
        self.is_patron: bool = False or kwargs.get("ispatron")
        self.is_super_patron: bool = False or kwargs.get("issuperpatron")
        self.is_banned: bool = False or kwargs.get("isbanned")
        self.is_mod: bool = False or kwargs.get("ismod")
        self.is_data_mod: bool = False or kwargs.get("isdatamod")
        self.is_translator: bool = False or kwargs.get("istranslator")
        self.is_proofreader: bool = False or kwargs.get("isproofreader")
        self.balance = int(kwargs.get("balance")) or 0
        self.xp = kwargs.get("xp") or 0
        access_id = kwargs.get("access")
        self.api_access: Optional[Access] = None if access_id is None else Access(access_id)
        self.gg_filter_active = False or kwargs.get("ggfilteractive")
        self.language = "en-US" or kwargs.get("language")
        self.lastfm = None or kwargs.get("lastfmusername")
        self.timezone = None or kwargs.get("timezone")
        self.rob_level = kwargs.get("roblevel") or 0
        self.daily_level = kwargs.get("dailylevel") or 0
        self.beg_level = kwargs.get("beglevel") or 0
        self.profile_level = kwargs.get("profilelevel") or 0
        _users[self.id] = self
        ...

    async def set_patron(self, active=True):
        """
        Add or Revoke a user's patron status.

        :param active: Whether the status should be active.
        """
        callback = CallBack(request={
            'route': 'user/patron_status/$user_id',
            'user_id': self.id,
            'method': 'POST' if active else 'DELETE',
        })
        await outer.client.add_and_wait(callback)
        self.is_patron = active

    async def add_token(self, unhashed_token, access: Access):
        """
        Add an API token to a user.

        :param unhashed_token:
        :param access: (Access) An Access object that is predefined in models/access
        """
        callback = CallBack(request={
            'route': 'user/token/$user_id',
            'user_id': self.id,
            'unhashed_token': unhashed_token,
            'access_id': access.id,
            'method': 'POST',
        })
        await outer.client.add_and_wait(callback)
        self.api_access = access

    async def delete_token(self):
        """
        Delete the user's current API token if they have one.
        """
        callback = CallBack(request={
            'route': 'user/token/$user_id',
            'user_id': self.id,
            'method': 'DELETE',
        })
        await outer.client.add_and_wait(callback)
        self.api_access = None

    async def set_super_patron(self, active=True):
        """
        Add or Revoke a user's super patron status.

        :param active: Whether the status should be active.
        """
        callback = CallBack(request={
            'route': 'user/superpatron_status/$user_id',
            'user_id': self.id,
            'method': 'POST' if active else 'DELETE',
        })
        await outer.client.add_and_wait(callback)
        self.is_super_patron = active
        self.is_patron = active  # remove their patron status from cache as well

    async def set_mod(self, active=True):
        """
        Add or Revoke a user's moderator status.

        :param active: Whether the status should be active.
        """
        callback = CallBack(request={
            'route': 'user/mod_status/$user_id',
            'user_id': self.id,
            'method': 'POST' if active else 'DELETE',
        })
        await outer.client.add_and_wait(callback)
        self.is_mod = active

    async def set_data_mod(self, active=True):
        """
        Add or Revoke a user's data moderator status.

        :param active: Whether the status should be active.
        """
        callback = CallBack(request={
            'route': 'user/data_mod_status/$user_id',
            'user_id': self.id,
            'method': 'POST' if active else 'DELETE',
        })
        await outer.client.add_and_wait(callback)
        self.is_data_mod = active

    async def set_proofreader(self, active=True):
        """
        Add or Revoke a user's proofreader status.

        :param active: Whether the status should be active.
        """
        callback = CallBack(request={
            'route': 'user/proofreader_status/$user_id',
            'user_id': self.id,
            'method': 'POST' if active else 'DELETE',
        })
        await outer.client.add_and_wait(callback)
        self.is_proofreader = active

    async def set_translator(self, active=True):
        """
        Add or Revoke a user's translator status.

        :param active: Whether the status should be active.
        """
        callback = CallBack(request={
            'route': 'user/translator_status/$user_id',
            'user_id': self.id,
            'method': 'POST' if active else 'DELETE',
        })
        await outer.client.add_and_wait(callback)
        self.is_translator = active

    async def set_ban(self, active=True):
        """
        Ban or Unban the user from the bot.

        :param active: (bool) Whether the ban should be active.
        """
        callback = CallBack(request={
            'route': 'user/ban_status/$user_id',
            'user_id': self.id,
            'method': 'POST' if active else 'DELETE',
        })
        await outer.client.add_and_wait(callback)
        self.is_banned = active

    @staticmethod
    async def add(user_id: int):
        """
        Add a user to the database.

        This will happen automatically when attempting to fetch a user's name that does not exist.

        :param user_id: The user ID to add.
        """
        callback = CallBack(request={
            'route': 'user/$user_id',
            'user_id': user_id,
            'method': 'POST',
        })

        await outer.client.add_and_wait(callback)

    @staticmethod
    async def delete(user_id: int):
        """
        Delete a user from the database and wipe all the information about them.

        The user object will be removed from cache if it is the target user.

        :param user_id: The user ID to delete.
        """
        callback = CallBack(request={
            'route': 'user/$user_id',
            'user_id': user_id,
            'method': 'DELETE',
        })

        await outer.client.add_and_wait(callback)

        try:
            # remove user from cache
            _users.pop(user_id)
        except KeyError:
            ...

    @staticmethod
    async def get(user_id: int):
        """Get a User object.

        If the User object does not exist in cache, it will fetch the user from the API.
        :param user_id: (int) The ID of the user to get/fetch.
        """
        existing_user = _users.get(user_id)
        if not existing_user:
            return await User.fetch(user_id)

    @staticmethod
    async def fetch(user_id: int = 0):
        """Fetch updated User objects from the API.

        If the user is not in the DB, it will add it.

        :param user_id: (int) The user name to fetch. Will fetch all users if set to 0.
        """
        # NOTE: User objects are added to cache on creation.
        callback = CallBack(request={
            'route': 'user/$user_id',
            'user_id': user_id,
            'method': 'GET'}
        )

        await outer.client.add_and_wait(callback)

        if user_id == 0:
            if not callback.response["results"]:
                return []

            return [User(user_info['userid'], **user_info) for user_info in callback.response["results"]]

        else:
            # return single user.
            if not callback.response["results"]:
                await User.add(user_id)

                return await User.fetch(user_id)  # recursive
            return User(callback.response["results"]['userid'], **callback.response["results"])


_users: Dict[int, User] = dict()
