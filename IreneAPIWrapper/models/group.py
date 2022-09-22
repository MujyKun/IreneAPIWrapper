from typing import Union, List, Optional, Dict, TYPE_CHECKING

from IreneAPIWrapper.sections import outer
from . import (
    CallBack,
    Access,
    AbstractModel,
    internal_fetch,
    internal_fetch_all,
    MediaSource,
    Date,
    Company,
    Display,
    Social,
    Tag,
    internal_delete,
    internal_insert,
)

if TYPE_CHECKING:
    from . import Affiliation, GroupAlias


class Group(AbstractModel):
    r"""Represents a Group object.

    A Group object inherits from :ref:`AbstractModel`.

    Parameters
    ----------
    group_id: int
        The group's unique ID.
    name: str
        The name of the group.
    date: :ref:`Date`
        The creation and disbandment of the group.
    description: str
        An overall description of the group.
    company: :ref:`Company`
        The company that owns the group.
    display: :ref:`Display`
        The display media (avatar & banner) for the group.
    website: str
        A custom website for the group.
    social: :ref:`Social`
        The social media associated with the group.
    media_count: int
        The media a group has.
    tags: List[:ref:`Tag`]
        The tags that affiliated with the group.
    aliases: List[:ref:`GroupAlias`]
        Aliases of the group.

    Attributes
    ----------
    id: int
        The group's unique ID.
    name: str
        The name of the group.
    date: :ref:`Date`
        The creation and disbandment of the group.
    description: str
        An overall description of the group.
    company: :ref:`Company`
        The company that owns the group.
    display: :ref:`Display`
        The display media (avatar & banner) for the group.
    website: str
        A custom website for the group.
    social: :ref:`Social`
        The social media associated with the group.
    media_count: int
        The media a group has.
    tags: List[:ref:`Tag`]
        The tags that affiliated with the group.
    aliases: List[:ref:`GroupAlias`]
        Aliases of the group.
    affiliations: List[:ref:`Affiliation`]
        All affiliations that are associated with the Group.

    """

    def __init__(
        self,
        group_id,
        name,
        date,
        description,
        company,
        display,
        website,
        social,
        media_count,
        tags,
        aliases,
    ):
        super(Group, self).__init__(group_id)
        self.name: str = name
        self.date: Date = date
        self.description = description
        self.company: Company = company
        self.display: Display = display
        self.website: str = website
        self.social: Social = social
        self.media_count: int = media_count or 0
        self.tags: List[Tag] = tags
        self.aliases: List[GroupAlias] = aliases
        self.affiliations: List[Affiliation] = []
        if not _groups.get(self.id):
            _groups[self.id] = self

    @staticmethod
    def priority():
        return 1

    async def get_card(self, markdown=False, extra=True):
        card_data = []
        if self.id:
            card_data.append(f"Group ID: {self.id}")
        if self.name:
            card_data.append(f"Group Name: {self.name}")
        if self.description:
            card_data.append(f"Description: {self.description}")

        if not extra:
            return card_data

        if self.date:
            date_card = await self.date.get_card(markdown=markdown)
            [card_data.append(info) for info in date_card]
        if self.company:
            company_card = await self.company.get_card(markdown=markdown)
            [card_data.append(info) for info in company_card]
        if self.display:
            display_card = await self.display.get_card(markdown=markdown)
            [card_data.append(info) for info in display_card]
        if self.website:
            card_data.append(
                f"Custom Website: {self.website}"
            ) if not markdown else card_data.append(f"[Custom Website]({self.website})")
        if self.social:
            social_card = await self.social.get_card(markdown=markdown)
            [card_data.append(info) for info in social_card]
        if self.tags:
            tags = ", ".join([str(tag) for tag in self.tags])
            card_data.append(f"Tags: {tags}")
        if self.aliases:
            aliases = ", ".join([str(alias) for alias in self.aliases])
            card_data.append(f"Aliases: {aliases}")
        if self.affiliations:
            affiliations = "\n".join([str(aff) for aff in self.affiliations])
            card_data.append(f"Affiliations:\n{affiliations}")
        return card_data

    @staticmethod
    async def create(*args, **kwargs):
        """
        Create a Group object.

        :return: :ref:`Group`
        """
        group_id = kwargs.get("groupid")
        name = kwargs.get("name")

        date_id = kwargs.get("dateid")
        date = await Date.get(date_id)

        description = kwargs.get("description")

        company_id = kwargs.get("companyid")
        company = await Company.get(company_id)

        display_id = kwargs.get("displayid")
        display = await Display.get(display_id)

        website = kwargs.get("website")

        social_id = kwargs.get("socialid")
        social = await Social.get(social_id)

        media_count = kwargs.get("mediacount")

        tag_ids = kwargs.get("tagids")
        tags = [] if not tag_ids else [await Tag.get(tag_id) for tag_id in tag_ids]

        alias_ids = kwargs.get("aliasids")

        # avoiding circular import when updating cache on GroupAlias insertions.
        from . import GroupAlias

        aliases = (
            []
            if not alias_ids
            else [await GroupAlias.get(alias_id) for alias_id in alias_ids]
        )

        Group(
            group_id,
            name,
            date,
            description,
            company,
            display,
            website,
            social,
            media_count,
            tags,
            aliases,
        )
        return _groups[group_id]

    def __str__(self):
        return self.name

    async def get_aliases_as_strings(self) -> List:
        return [alias.name for alias in self.aliases]

    async def delete(self) -> None:
        """
        Delete the Group object from the database and remove it from cache.

        :returns: None
        """
        await internal_delete(
            self,
            request={
                "route": "group/$group_id",
                "group_id": self.id,
                "method": "DELETE",
            },
        )
        await self._remove_from_cache()

    async def _remove_from_cache(self) -> None:
        """
        Remove the Group object from cache.

        :returns: None
        """
        _groups.pop(self.id)

    @staticmethod
    async def insert(
        group_name: str,
        date_id: int = None,
        description: str = None,
        company_id: int = None,
        display_id: int = None,
        website: str = None,
        social_id: int = None,
        tag_ids: List[int] = None,
    ) -> None:
        """
        Insert a new group into the database.

        :param group_name: str
            The group's name.
        :param date_id: int
            :ref:`Date` ID including the creation and disbandment dates.
        :param description: str
            Description of the overall group.
        :param company_id: int
            ID of the :ref:`Company` the group belongs to.
        :param display_id: int
            ID of the :ref:`Display` the group is associated with.
        :param website: str
            A custom website for the group.
        :param social_id: int
            ID of the :ref:`Social` the group has.
        :param tag_ids: List[int]
            A list of :ref:`Tag` IDs.
        :return: None
        """
        await internal_insert(
            request={
                "route": "group",
                "group_name": group_name,
                "date_id": date_id,
                "description": description,
                "company_id": company_id,
                "display_id": display_id,
                "website": website,
                "social_id": social_id,
                "tag_ids": tag_ids,
                "method": "POST",
            }
        )

    @staticmethod
    async def get(group_id: int, fetch=True):
        """Get a :ref:`Group` object.

        If the :ref:`Group` object does not exist in cache, it will fetch the name from the API.
        :param group_id: int
            The ID of the :ref:`Group` to get/fetch.
        :param fetch: bool
            Whether to fetch from the API if not found in cache.
        :returns: :ref:`Group`
        """
        existing = _groups.get(group_id)
        if not existing and fetch:
            return await Group.fetch(group_id)
        return existing

    @staticmethod
    async def get_all():
        """
        Get all Group objects in cache.

        :returns: dict_values[:ref:`Group`]
            All Group objects from cache.
        """
        return _groups.values()

    @staticmethod
    async def fetch(group_id: int):
        """Fetch an updated Group object from the API.

        .. NOTE::: Group objects are added to cache on creation.

        :param group_id: int
            The group's ID to fetch.
        :returns: :ref:`Group`
        """
        return await internal_fetch(
            obj=Group,
            request={"route": "group/$group_id", "group_id": group_id, "method": "GET"},
        )

    @staticmethod
    async def fetch_all():
        """Fetch all groups.

        .. NOTE::: Group objects are added to cache on creation.
        """
        return await internal_fetch_all(
            obj=Group, request={"route": "group/", "method": "GET"}
        )


_groups: Dict[int, Group] = dict()
