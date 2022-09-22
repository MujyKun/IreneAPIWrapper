from typing import Union, List, Optional, Dict

from IreneAPIWrapper.sections import outer
from . import (
    CallBack,
    Access,
    AbstractModel,
    internal_fetch,
    internal_fetch_all,
    MediaSource,
    User,
    internal_insert,
    internal_delete,
    basic_call,
)


class Guild(AbstractModel):
    r"""Represents a Guild object.

    A Guild inherits from :ref:`AbstractModel`.

    Parameters
    ----------
    guild_id: int
        The guild's id.
    name: str
        The guild name.
    emoji_count: int
        Current amount of emojis on the guild.
    afk_timeout: int
        The time before a User gets timed out in a voice channel.
    icon: str
        The Guild's icon.
    owner_id: int
        The guild owner's id.
    owner: :ref:`User`
        A reference to the guild owner's User object.
    banner: str
        A banner of the guild.
    description: str
        A description of the guild.
    mfa_level: int
        MFA level of the guild.
    splash: str
        Splash Art of the guild.
    nitro_level: int
        Current nitro level of the guild.
    boosts: int
        Number of times the guild has been boosted.
    text_channel_count: int
        Amount of text channels the guild has.
    voice_channel_count: int
        Amount of voice channels the guild has.
    category_count: int
        Amount of categories the guild has.
    emoji_limit: int
        Maximum amount of emojis the guild can have.
    member_count: int
        Amount of users the guild has.
    role_count: int
        Amount of roles the guild has.
    shard_id: int
        The shard connected to the guild.
    create_date: str
        The date the guild was created.
    has_bot: bool
        Whether the bot exists in the guild.
    prefixes: Optional[List[str]]
        A list of prefixes the guild uses.

    Attributes
    ----------
    id: int
        The guild's id.
    name: str
        The guild name.
    emoji_count: int
        Current amount of emojis on the guild.
    afk_timeout: int
        The time before a User gets timed out in a voice channel.
    icon: str
        The Guild's icon.
    owner_id: int
        The guild owner's id.
    owner: :ref:`User`
        A reference to the guild owner's User object.
    banner: str
        A banner of the guild.
    description: str
        A description of the guild.
    mfa_level: int
        MFA level of the guild.
    splash: str
        Splash Art of the guild.
    nitro_level: int
        Current nitro level of the guild.
    boosts: int
        Number of times the guild has been boosted.
    text_channel_count: int
        Amount of text channels the guild has.
    voice_channel_count: int
        Amount of voice channels the guild has.
    category_count: int
        Amount of categories the guild has.
    emoji_limit: int
        Maximum amount of emojis the guild can have.
    member_count: int
        Amount of users the guild has.
    role_count: int
        Amount of roles the guild has.
    shard_id: int
        The shard connected to the guild.
    create_date: str
        The date the guild was created.
    has_bot: bool
        Whether the bot exists in the guild.
    prefixes: Optional[List[str]]
        A list of prefixes the guild uses.
    """

    def __init__(
        self,
        guild_id,
        name,
        emoji_count,
        afk_timeout,
        icon,
        owner_id,
        owner,
        banner,
        description,
        mfa_level,
        splash,
        nitro_level,
        boosts,
        text_channel_count,
        voice_channel_count,
        category_count,
        emoji_limit,
        member_count,
        role_count,
        shard_id,
        create_date,
        has_bot,
        prefixes=None,
    ):
        super(Guild, self).__init__(guild_id)
        self.name = name
        self.emoji_count = emoji_count
        self.afk_timeout = afk_timeout
        self.icon = icon
        self.owner_id = owner_id
        self.owner = owner
        self.banner = banner
        self.description = description
        self.mfa_level = mfa_level
        self.splash = splash
        self.nitro_level = nitro_level
        self.boosts = boosts
        self.text_channel_count = text_channel_count
        self.voice_channel_count = voice_channel_count
        self.category_count = category_count
        self.emoji_limit = emoji_limit
        self.member_count = member_count
        self.role_count = role_count
        self.shard_id = shard_id
        self.create_date = create_date
        self.has_bot = has_bot
        self.prefixes: List[str] = prefixes or []
        if not _guilds.get(self.id):
            _guilds[self.id] = self

    @staticmethod
    def priority():
        return 3

    @staticmethod
    async def create(*args, **kwargs):
        """
        Create a Guild object.

        :returns: :ref:`Guild`
        """
        guild_id = kwargs.get("guildid")
        name = kwargs.get("name")
        emoji_count = kwargs.get("emojicount")
        afk_timeout = kwargs.get("afktimeout")
        icon = kwargs.get("icon")

        owner_id = kwargs.get("ownerid")
        owner = await User.get(owner_id)

        banner = kwargs.get("banner")
        description = kwargs.get("description")
        mfa_level = kwargs.get("mfalevel")
        splash = kwargs.get("splash")
        nitro_level = kwargs.get("nitrolevel")
        boosts = kwargs.get("boosts")
        text_channel_count = kwargs.get("textchannelcount")
        voice_channel_count = kwargs.get("voicechannelcount")
        category_count = kwargs.get("categorycount")
        emoji_limit = kwargs.get("emojilimit")
        member_count = kwargs.get("membercount")
        role_count = kwargs.get("rolecount")
        shard_id = kwargs.get("shardid")
        create_date = kwargs.get("createdate")
        has_bot: bool = kwargs.get("hasbot")
        prefixes = kwargs.get("prefixes")

        if prefixes:
            prefixes = list(prefixes)

        Guild(
            guild_id,
            name,
            emoji_count,
            afk_timeout,
            icon,
            owner_id,
            owner,
            banner,
            description,
            mfa_level,
            splash,
            nitro_level,
            boosts,
            text_channel_count,
            voice_channel_count,
            category_count,
            emoji_limit,
            member_count,
            role_count,
            shard_id,
            create_date,
            has_bot,
            prefixes,
        )
        return _guilds[guild_id]

    async def add_prefix(self, prefix: str) -> None:
        """Add a guild prefix.

        :param prefix: str
            The prefix to add.
        """
        prefix = prefix.lower()
        if prefix in self.prefixes:
            return

        await basic_call(
            request={
                "route": "guild/prefix/$guild_id",
                "guild_id": self.id,
                "prefix": prefix,
                "method": "POST",
            }
        )

        self.prefixes.append(prefix)

    async def delete_prefix(self, prefix: str) -> None:
        """Delete a guild prefix.

        :param prefix: str
            The prefix to delete.
        """
        prefix = prefix.lower()
        if prefix not in self.prefixes:
            return

        await basic_call(
            request={
                "route": "guild/prefix/$guild_id",
                "guild_id": self.id,
                "prefix": prefix,
                "method": "DELETE",
            }
        )

        self.prefixes.remove(prefix)

    async def fetch_prefixes(self) -> List[str]:
        """Get a list of prefixes for the guild from the API.

        :return: List[str]
        """
        callback = await basic_call(
            request={
                "route": "guild/prefix/$guild_id",
                "guild_id": self.id,
                "method": "GET",
            }
        )
        prefixes = callback.response.get("results")
        if prefixes:
            self.prefixes: List[str] = list(prefixes)
        return prefixes  # returns response from the api, not cache.

    @staticmethod
    async def fetch_all_prefixes() -> Dict[int, List[str]]:
        """Fetch all prefixes.

        :return: Dict[int, List[str]]
        """
        callback = await basic_call(request={"route": "guild/prefix/", "method": "GET"})

        return callback.response.get("results")

    async def delete(self) -> None:
        """
        Delete the Guild object from the database and remove it from cache.

        :returns: None
        """
        await internal_delete(
            self,
            request={
                "route": "guild/$guild_id",
                "guild_id": self.id,
                "method": "DELETE",
            },
        )
        await self._remove_from_cache()

    async def _remove_from_cache(self) -> None:
        """
        Remove the Guild object from cache.

        :returns: None
        """
        _guilds.pop(self.id)

    @staticmethod
    async def insert(
        guild_id,
        name=None,
        emoji_count=None,
        afk_timeout=None,
        icon=None,
        owner_id=None,
        banner=None,
        description=None,
        mfa_level=None,
        splash=None,
        nitro_level=None,
        boosts=None,
        text_channel_count=None,
        voice_channel_count=None,
        category_count=None,
        emoji_limit=None,
        member_count=None,
        role_count=None,
        shard_id=None,
        create_date=None,
        has_bot=True,
    ):
        r"""
        Insert a new Guild into the database.


        Parameters
        ----------

        guild_id: int
            The guild's ID.
        name: str
            Name of the guild.
        emoji_count: int
            Number of emojis the guild has.
        afk_timeout: int
            Guild AFK timeout for voice channels
        icon: str
            Icon URL of the guild.
        owner_id: int
            Owner ID of the guild.
        banner: str
            Banner of the guild.
        description: str
            Guild description.
        mfa_level: int
            MFA level of the guild.
        splash: str
            Splash art url of the guild.
        nitro_level: int
            Nitro level of the guild.
        boosts: int
            Number of boosts the guild has.
        text_channel_count: int
            Number of text channels the guild has.
        voice_channel_count: int
            Number of voice channels the guild has.
        category_count: int
            Number of categories the guild has.
        emoji_limit: int
            Maximum number of emojis allowed in the guild.
        member_count: int
            The number of members in the guild.
        role_count: int
            The number of roles in the guild.
        shard_id: int
            The shard the guild is connected to.
        create_date: timestamp
            The creation date of the Guild.
        has_bot: bool
            Whether the guild has the bot.

        :returns: None
        """
        await internal_insert(
            request={
                "route": "guild",
                "guild_id": guild_id,
                "name": name,
                "emoji_count": emoji_count,
                "afk_timeout": afk_timeout,
                "icon": icon,
                "owner_id": owner_id,
                "banner": banner,
                "description": description,
                "mfa_level": mfa_level,
                "splash": splash,
                "nitro_level": nitro_level,
                "boosts": boosts,
                "text_channel_count": text_channel_count,
                "voice_channel_count": voice_channel_count,
                "category_count": category_count,
                "emoji_limit": emoji_limit,
                "member_count": member_count,
                "role_count": role_count,
                "shard_id": shard_id,
                "create_date": str(create_date),
                "has_bot": has_bot,
                "method": "POST",
            }
        )

    @staticmethod
    async def get(guild_id: int, fetch=True):
        """Get a Guild object.

        If the Guild object does not exist in cache, it will fetch the name from the API.
        :param guild_id: int
            The ID of the guild to get/fetch.
        :param fetch: bool
            Whether to fetch from the API if not found in cache.
        :returns: :ref:`Guild`
        """
        existing = _guilds.get(guild_id)
        if not existing and fetch:
            return await Guild.fetch(guild_id)
        return existing

    @staticmethod
    async def get_all():
        """
        Get all Guild objects in cache.

        :returns: dict_values[:ref:`Guild`]
            All Guild objects from cache.
        """
        return _guilds.values()

    @staticmethod
    async def fetch(guild_id: int):
        """Fetch an updated Guild object from the API.

        .. NOTE::: Guild objects are added to cache on creation.

        :param guild_id: int
            The guild's ID to fetch.
        :returns: :ref:`Guild`
        """
        return await internal_fetch(
            obj=Guild,
            request={"route": "guild/$guild_id", "guild_id": guild_id, "method": "GET"},
        )

    @staticmethod
    async def fetch_all():
        """
        Fetch all Guild objects from the API.

        :returns: List[:ref:`Guild`]
        """
        return await internal_fetch(
            obj=Guild, request={"route": "guild/", "method": "GET"}
        )


_guilds: Dict[int, Guild] = dict()
