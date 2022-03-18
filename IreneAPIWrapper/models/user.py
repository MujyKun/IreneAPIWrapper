from typing import Union, List, Optional, Dict

from IreneAPIWrapper.sections import outer
from . import CallBack, Access, AbstractModel, internal_fetch, internal_fetch_all, internal_insert, internal_delete


class User(AbstractModel):
    def __init__(self, user_id, is_patron, is_super_patron, is_banned, is_mod, is_data_mod, is_translator,
                 is_proofreader, balance, xp, api_access, gg_filter_active, language, lastfm, timezone,
                 rob_level, daily_level, beg_level, profile_level):
        super(User, self).__init__(user_id)
        self.is_patron: bool = is_patron
        self.is_super_patron: bool = is_super_patron
        self.is_banned: bool = is_banned
        self.is_mod: bool = is_mod
        self.is_data_mod: bool = is_data_mod
        self.is_translator: bool = is_translator
        self.is_proofreader: bool = is_proofreader
        self.balance: int = balance
        self.xp: int = xp
        self.api_access: Optional[Access] = api_access
        self.gg_filter_active: bool = gg_filter_active
        self.language: str = language
        self.lastfm: str = lastfm
        self.timezone: str = timezone
        self.rob_level: int = rob_level
        self.daily_level: int = daily_level
        self.beg_level: int = beg_level
        self.profile_level: int = profile_level
        _users[self.id] = self

    @staticmethod
    async def create(*args, **kwargs):
        """
        Create a User object.

        :returns: :ref:`User`
        """
        user_id: int = kwargs.get("userid")
        is_patron: bool = False or kwargs.get("ispatron")
        is_super_patron: bool = False or kwargs.get("issuperpatron")
        is_banned: bool = False or kwargs.get("isbanned")
        is_mod: bool = False or kwargs.get("ismod")
        is_data_mod: bool = False or kwargs.get("isdatamod")
        is_translator: bool = False or kwargs.get("istranslator")
        is_proofreader: bool = False or kwargs.get("isproofreader")
        balance = int(kwargs.get("balance")) or 0
        xp = kwargs.get("xp") or 0
        access_id = kwargs.get("access")
        api_access: Optional[Access] = None if access_id is None else Access(access_id)
        gg_filter_active = False or kwargs.get("ggfilteractive")
        language = "en-US" or kwargs.get("language")
        lastfm = None or kwargs.get("lastfmusername")
        timezone = None or kwargs.get("timezone")
        rob_level = kwargs.get("roblevel") or 0
        daily_level = kwargs.get("dailylevel") or 0
        beg_level = kwargs.get("beglevel") or 0
        profile_level = kwargs.get("profilelevel") or 0
        return User(user_id, is_patron, is_super_patron, is_banned, is_mod, is_data_mod, is_translator,
                    is_proofreader, balance, xp, api_access, gg_filter_active, language, lastfm, timezone,
                    rob_level, daily_level, beg_level, profile_level)

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
    async def insert(user_id: int):
        """
        Add a user to the database.

        :param user_id: The user ID to add.

        :returns: None
        """
        callback = CallBack(request={
            'route': 'user/$user_id',
            'user_id': user_id,
            'method': 'POST',
        })

        await outer.client.add_and_wait(callback)

    async def delete(self) -> None:
        """
        Delete a user from the database and wipe all the information about them.

        :returns: None
        """
        await internal_delete(self, request={
            'route': 'user/$user_id',
            'user_id': self.id,
            'method': 'DELETE',
        })
        await self._remove_from_cache()

    async def _remove_from_cache(self) -> None:
        """
        Remove the User object from cache.

        :returns: None
        """
        _users.pop(self.id)

    @staticmethod
    async def get(user_id: int, fetch=True):
        """Get a User object.

        If the User object does not exist in cache, it will fetch the user from the API.
        :param user_id: int
            The ID of the user to get/fetch.
        :param fetch: bool
            Whether to fetch from the API if not found in cache.
        :returns: :ref:`User`
        """
        existing = _users.get(user_id)
        if not existing and fetch:
            return await User.fetch(user_id)
        return existing

    @staticmethod
    async def fetch(user_id: int):
        """Fetch an updated User object from the API.

        If the user is not in the DB, it will add it.
        # NOTE: User objects are added to cache on creation.

        :param user_id: int
            The user's ID to fetch.
        :returns: :ref:`User`
        """
        return await internal_fetch(obj=User, request={
            'route': 'user/$user_id',
            'user_id': user_id,
            'method': 'GET'})

    @staticmethod
    async def fetch_all():
        """Fetch all users.

        # NOTE: User objects are added to cache on creation.
        """
        return await internal_fetch_all(User, request={
            'route': 'user/',
            'method': 'GET'}
        )


_users: Dict[int, User] = dict()
