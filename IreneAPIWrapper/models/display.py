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


class Display(AbstractModel):
    r"""Represents the images involved with an entity's profile such as an avatar or banner.

    A Display object inherits from :ref:`AbstractModel`.

    Parameters
    ----------
    display_id: int
        The Affiliation id.
    avatar: :ref:`MediaSource`
        The person that is affiliated with a Group.
    banner: :ref:`MediaSource`
        The group that the Person is affiliated with.

    Attributes
    ----------
    id: int
        The Display id.
    avatar: :ref:`MediaSource`
        The person that is affiliated with a Group.
    banner: :ref:`MediaSource`
        The group that the Person is affiliated with.

    """

    def __init__(
        self, display_id, avatar: MediaSource, banner: MediaSource, *args, **kwargs
    ):
        super(Display, self).__init__(display_id)
        self.avatar: MediaSource = avatar
        self.banner: MediaSource = banner
        if not _displays.get(self.id):
            _displays[self.id] = self

    async def get_card(self, markdown=False):
        card_data = []
        if self.avatar:
            card_data.append(
                f"Avatar: {self.avatar.url}"
            ) if not markdown else card_data.append(f"[Avatar]({self.avatar.url})")
        if self.banner:
            card_data.append(
                f"Banner: {self.banner.url}"
            ) if not markdown else card_data.append(f"[Banner]({self.banner.url})")
        return card_data

    @staticmethod
    async def create(*args, **kwargs):
        """
        Create a Display object.

        :returns: :ref:`Display`
        """
        display_id = kwargs.get("displayid")
        avatar = MediaSource(kwargs.get("avatar"))
        banner = MediaSource(kwargs.get("banner"))
        Display(display_id, avatar, banner)
        return _displays[display_id]

    async def delete(self) -> None:
        """Delete the Display object from the database and remove it from cache."""
        await internal_delete(
            self,
            request={
                "route": "display/$display_id",
                "display_id": self.id,
                "method": "DELETE",
            },
        )
        await self._remove_from_cache()

    async def _remove_from_cache(self) -> None:
        """Remove the Display object from cache."""
        _displays.pop(self.id)

    @staticmethod
    async def insert(avatar: str, banner: str) -> None:
        """
        Insert a new display into the database.

        :param avatar: str
            The avatar for the entity.
        :param banner: str
            The banner for the entity.
        :return: None
        """
        await internal_insert(
            request={
                "route": "display",
                "avatar": avatar,
                "banner": banner,
                "method": "POST",
            }
        )

    @staticmethod
    async def get(display_id: int, fetch=True):
        """Get a Display object.

        If the Display object does not exist in cache, it will fetch the name from the API.
        :param display_id: int
            The ID of the display to get/fetch.
        :param fetch: bool
            Whether to fetch from the API if not found in cache.
        :returns: Optional[:ref:`Display`]
            The display object requested.
        """
        existing = _displays.get(display_id)
        if not existing:
            return await Display.fetch(display_id)
        return existing

    @staticmethod
    async def get_all():
        """
        Get all Display objects in cache.

        :returns: dict_values[:ref:`Display`]
            All Display objects from cache.
        """
        return _displays.values()

    @staticmethod
    async def fetch(display_id: int):
        """Fetch an updated Display object from the API.

        .. NOTE::: Display objects are added to cache on creation.

        :param display_id: int
            The display's ID to fetch.
        :returns: Optional[:ref:`Display`]
            The display object requested.
        """
        return await internal_fetch(
            obj=Display,
            request={
                "route": "display/$display_id",
                "display_id": display_id,
                "method": "GET",
            },
        )

    @staticmethod
    async def fetch_all():
        """Fetch all displays.

        .. NOTE::: Display objects are added to cache on creation.
        """
        return await internal_fetch_all(
            obj=Display, request={"route": "display/", "method": "GET"}
        )


_displays: Dict[int, Display] = dict()
