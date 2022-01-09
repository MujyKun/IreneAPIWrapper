from typing import Union, List, Optional, Dict

from IreneAPIWrapper.sections import outer
from . import CallBack, Access, AbstractModel, internal_fetch, internal_fetch_all, MediaSource


class Social(AbstractModel):
    def __init__(self, social_id, twitter, youtube, melon, instagram, vlive, spotify, fancafe, facebook, tiktok):
        super(Social, self).__init__()
        self.id = social_id
        self.twitter = twitter
        self.youtube = youtube
        self.melon = melon
        self.instagram = instagram
        self.vlive = vlive
        self.spotify = spotify
        self.fancafe = fancafe
        self.facebook = facebook
        self.tiktok = tiktok

        _socials[self.id] = self

    @staticmethod
    async def create(*args, **kwargs):
        # TODO: Create
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

        return Social(social_id, twitter, youtube, melon, instagram, vlive, spotify, fancafe, facebook, tiktok)

    @staticmethod
    async def get(social_id: int, fetch=True):
        """Get a Social object.

        If the Social object does not exist in cache, it will fetch the name from the API.
        :param social_id: (int) The ID of the name to get/fetch.
        :param fetch: (bool) Whether to fetch from the API if not found in cache.
        """
        existing = _socials.get(social_id)
        if not existing and fetch:
            return await Social.fetch(social_id)
        return existing

    @staticmethod
    async def fetch(social_id: int):
        """Fetch an updated Social object from the API.

        # NOTE: Social objects are added to cache on creation.

        :param social_id: (int) The social's ID to fetch.
        """
        return await internal_fetch(obj=Social, request={
            'route': 'social/$social_id',
            'social_id': social_id,
            'method': 'GET'}
        )

    @staticmethod
    async def fetch_all():
        """Fetch all socials.

        # NOTE: Social objects are added to cache on creation.
        """
        return await internal_fetch_all(obj=Social, request={
            'route': 'social/',
            'method': 'GET'}
        )


_socials: Dict[int, Social] = dict()
