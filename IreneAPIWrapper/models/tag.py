from typing import Union, List, Optional, Dict

from IreneAPIWrapper.sections import outer
from . import CallBack, Access, AbstractModel, internal_fetch, internal_fetch_all


class Tag(AbstractModel):
    def __init__(self, tag_id, name, *args, **kwargs):
        super(Tag, self).__init__()
        self.id = tag_id
        self.name = name
        _tags[self.id] = self

    async def create(self, *args, **kwargs):
        tag_id = kwargs.get('tagid')
        name = kwargs.get('name')
        return Tag(tag_id, name)

    @staticmethod
    async def get(tag_id: int):
        """Get a Tag object.

        If the Tag object does not exist in cache, it will fetch the tag from the API.
        :param tag_id: (int) The ID of the tag to get/fetch.
        """
        existing_person = _tags.get(tag_id)
        if not existing_person:
            return await Tag.fetch(tag_id)

    @staticmethod
    async def fetch(tag_id: int):
        """Fetch an updated Tag object from the API.

        # NOTE: Tag objects are added to cache on creation.

        :param tag_id: (int) The tag's ID to fetch.
        """
        return internal_fetch(Tag, request={
            'route': 'tag/$tag_id',
            'tag_id': tag_id,
            'method': 'GET'})

    @staticmethod
    async def fetch_all():
        """Fetch all tags.

        # NOTE: Tag objects are added to cache on creation.
        """
        return internal_fetch_all(obj=Tag, request={
            'route': 'tag/',
            'method': 'GET'})


_tags: Dict[int, Tag] = dict()
