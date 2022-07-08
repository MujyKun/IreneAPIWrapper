from typing import Union, List, Optional, Dict

from IreneAPIWrapper.sections import outer
from . import (
    CallBack,
    Access,
    AbstractModel,
    internal_fetch,
    internal_fetch_all,
    MediaSource,
    internal_insert,
    internal_delete,
)


class Social(AbstractModel):
    r"""Represents the social media sources for an entity.

    A Social object inherits from :ref:`AbstractModel`.

    Parameters
    ----------
    social_id: int
        The Social ID
    twitter: str
        The Twitter code
    youtube: str
        The youtube code
    melon: str
        The melon code
    instagram: str
        The instagram code
    vlive: str
        The vlive code
    spotify: str
        The spotify code
    fancafe: str
        The fancafe code
    facebook: str
        The facebook code
    tiktok: str
        The tiktok code

    Attributes
    ----------
    id: int
        The Social ID
    twitter: str
        The Twitter code
    youtube: str
        The youtube code
    melon: str
        The melon code
    instagram: str
        The instagram code
    vlive: str
        The vlive code
    spotify: str
        The spotify code
    fancafe: str
        The fancafe code
    facebook: str
        The facebook code
    tiktok: str
        The tiktok code

    """

    def __init__(
        self,
        social_id,
        twitter,
        youtube,
        melon,
        instagram,
        vlive,
        spotify,
        fancafe,
        facebook,
        tiktok,
    ):
        super(Social, self).__init__(social_id)
        self.twitter = twitter
        self.youtube = youtube
        self.melon = melon
        self.instagram = instagram
        self.vlive = vlive
        self.spotify = spotify
        self.fancafe = fancafe
        self.facebook = facebook
        self.tiktok = tiktok

        if not _socials.get(self.id):
            _socials[self.id] = self

    @staticmethod
    async def create(*args, **kwargs):
        social_id = kwargs.get("socialid")
        twitter = kwargs.get("twitter")
        youtube = kwargs.get("youtube")
        melon = kwargs.get("melon")
        instagram = kwargs.get("instagram")
        vlive = kwargs.get("vlive")
        spotify = kwargs.get("spotify")
        fancafe = kwargs.get("fancafe")
        facebook = kwargs.get("facebook")
        tiktok = kwargs.get("tiktok")

        Social(
            social_id,
            twitter,
            youtube,
            melon,
            instagram,
            vlive,
            spotify,
            fancafe,
            facebook,
            tiktok,
        )
        return _socials[social_id]

    async def delete(self) -> None:
        """
        Delete the Social object from the database and remove it from cache.

        :returns: None
        """
        await internal_delete(
            self,
            request={
                "route": "social/$social_id",
                "social_id": self.id,
                "method": "DELETE",
            },
        )
        await self._remove_from_cache()

    async def _remove_from_cache(self) -> None:
        """
        Remove the Social object from cache.

        :returns: None
        """
        _socials.pop(self.id)

    @staticmethod
    async def insert(
        twitter, youtube, melon, instagram, vlive, spotify, fancafe, facebook, tiktok
    ) -> None:
        r"""
        Insert a new social into the database.

        Parameters
        ----------
        twitter: str
            Twitter Code
        youtube: str
            Youtube Code
        melon: str
            Melon code
        instagram: str
            Instagram code
        vlive: str
            Vlive code
        spotify: str
            Spotify code
        fancafe: str
            fancafe code
        facebook: str
            Facebook code
        tiktok: str
            Tiktok code

        :returns: None
        """
        await internal_insert(
            request={
                "route": "social",
                "twitter": twitter,
                "youtube": youtube,
                "melon": melon,
                "instagram": instagram,
                "vlive": vlive,
                "spotify": spotify,
                "fancafe": fancafe,
                "facebook": facebook,
                "tiktok": tiktok,
                "method": "POST",
            }
        )

    @staticmethod
    async def get(social_id: int, fetch=True):
        """Get a Social object.

        If the Social object does not exist in cache, it will fetch the name from the API.
        :param social_id: int
            The ID of the name to get/fetch.
        :param fetch: bool
            Whether to fetch from the API if not found in cache.
        :returns: :ref:`Social`
        """
        existing = _socials.get(social_id)
        if not existing and fetch:
            return await Social.fetch(social_id)
        return existing

    @staticmethod
    async def get_all():
        """
        Get all Social objects in cache.

        :returns: dict_values[:ref:`Social`]
            All Social objects from cache.
        """
        return _socials.values()

    @staticmethod
    async def fetch(social_id: int):
        """Fetch an updated Social object from the API.

        .. NOTE::: Social objects are added to cache on creation.

        :param social_id: int
            The social's ID to fetch.
        :returns: :ref:`Social`
        """
        return await internal_fetch(
            obj=Social,
            request={
                "route": "social/$social_id",
                "social_id": social_id,
                "method": "GET",
            },
        )

    @staticmethod
    async def fetch_all():
        """Fetch all socials.

        .. NOTE::: Social objects are added to cache on creation.
        """
        return await internal_fetch_all(
            obj=Social, request={"route": "social/", "method": "GET"}
        )


_socials: Dict[int, Social] = dict()
