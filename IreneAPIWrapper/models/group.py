from typing import Union, List, Optional, Dict

from IreneAPIWrapper.sections import outer
from . import CallBack, Access, AbstractModel, internal_fetch, internal_fetch_all, MediaSource, Date, Company, \
    Display, Social, Tag, GroupAlias


class Group(AbstractModel):
    def __init__(self, group_id, name, date, description, company, display, website, social, tags, aliases):
        super(Group, self).__init__()
        self.id: int = group_id
        self.name: str = name
        self.date: Date = date
        self.description = description
        self.company: Company = company
        self.display: Display = display
        self.website: str = website
        self.social: Social = social
        self.tags: List[Tag] = tags
        self.aliases: List[GroupAlias] = aliases
        _groups[self.id] = self

    @staticmethod
    async def create(*args, **kwargs):
        group_id = kwargs.get("groupid")
        name = kwargs.get("name")

        date_id = kwargs.get("dateid")
        date = await Date.get(date_id)

        description = kwargs.get("description")

        company_id = kwargs.get("companyid")
        company = Company.get(company_id)

        display_id = kwargs.get("displayid")
        display = Display.get(display_id)

        website = kwargs.get("website")

        social_id = kwargs.get("socialid")
        social = Social.get(social_id)

        tag_ids = kwargs.get("tagids")
        tags = [] if not tag_ids else [await Tag.get(tag_id) for tag_id in tag_ids]

        alias_ids = kwargs.get("aliases")
        aliases = [] if not alias_ids else [await GroupAlias.get(alias_id) for alias_id in alias_ids]

        group_args = {group_id, name, date, description, company, display, website, social, tags, aliases}

        return Group(*group_args)

    @staticmethod
    async def get(group_id: int):
        """Get a Group object.

        If the Group object does not exist in cache, it will fetch the name from the API.
        :param group_id: (int) The ID of the name to get/fetch.
        """
        existing_person = _groups.get(group_id)
        if not existing_person:
            return await Group.fetch(group_id)

    @staticmethod
    async def fetch(group_id: int):
        """Fetch an updated Group object from the API.

        # NOTE: Group objects are added to cache on creation.

        :param group_id: (int) The group's ID to fetch.
        """
        return internal_fetch(obj=Group, request={
            'route': 'group/$group_id',
            'group_id': group_id,
            'method': 'GET'}
        )

    @staticmethod
    async def fetch_all():
        """Fetch all groups.

        # NOTE: Group objects are added to cache on creation.
        """
        return internal_fetch_all(obj=Group, request={
            'route': 'group/',
            'method': 'GET'}
        )


_groups: Dict[int, Group] = dict()
