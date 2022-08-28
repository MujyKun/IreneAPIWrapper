from typing import Union, List, Optional, Dict

from IreneAPIWrapper.sections import outer
from . import (
    CallBack,
    Access,
    AbstractModel,
    internal_fetch,
    internal_fetch_all,
    MediaSource,
    Date,
    internal_delete,
    internal_insert,
)


class Company(AbstractModel):
    r"""Represents the business/company that exists for several entities.

    A Company object inherits from :ref:`AbstractModel`.

    Parameters
    ----------
    company_id: int
        The company's unique ID
    name: str
        The company's name.
    description: str
        A general description of the company as a whole.
    date: :ref:`Date`
        The Date object that involves the creation and retirement of the company.

    Attributes
    ----------
    id: int
        The company's unique ID
    name: str
        The company's name.
    description: str
        A general description of the company as a whole.
    date: :ref:`Date`
        The Date object that involves the creation and retirement of the company.

    """

    def __init__(self, company_id, name, description, date, *args, **kwargs):
        super(Company, self).__init__(company_id)
        self.name = name
        self.description = description
        self.date: Date = date
        if not _companies.get(self.id):
            _companies[self.id] = self

    async def get_card(self, markdown=False):
        card_data = []
        if self.id:
            card_data.append(f"Company ID: {self.id}")
        if self.name:
            card_data.append(f"Company Name: {self.name}")
        return card_data

    @staticmethod
    async def create(*args, **kwargs):
        """
        Create a Company object.

        :returns: :ref:`Company`
        """
        company_id = kwargs.get("companyid")
        name = kwargs.get("name")
        description = kwargs.get("description")

        date_id = kwargs.get("dateid")
        date = await Date.get(date_id)

        Company(company_id, name, description, date)
        return _companies[company_id]

    async def delete(self):
        """Delete the Company object from the database and remove it from cache."""
        await internal_delete(
            self,
            request={
                "route": "company/$company_id",
                "company_id": self.id,
                "method": "DELETE",
            },
        )
        await self._remove_from_cache()

    async def _remove_from_cache(self):
        """Remove the Company object from cache."""
        _companies.pop(self.id)

    @staticmethod
    async def insert(company_name, description, date: Date) -> None:
        """
        Insert a new company into the database.

        :param company_name: str
            The company's name.
        :param description:
            A description of the company as a whole.
        :param date:
            The :ref:`Date` object for the creation and retirement of the company.
        :return: None
        """
        await internal_insert(
            request={
                "route": "company",
                "name": company_name,
                "description": description,
                "date_id": date.id,
            }
        )

    @staticmethod
    async def get(company_id: int, fetch=True):
        """Get a Company object.

        If the Company object does not exist in cache, it will fetch the name from the API.
        :param company_id: int
            The ID of the company to get/fetch.
        :param fetch: bool
            Whether to fetch from the API if not found in cache.
        :returns: Optional[:ref:`Company`]
            The company object requested.
        """
        existing = _companies.get(company_id)
        if not existing and fetch:
            return await Company.fetch(company_id)
        return existing

    @staticmethod
    async def get_all():
        """
        Get all Company objects in cache.

        :returns: dict_values[:ref:`Company`]
            All Company objects from cache.
        """
        return _companies.values()

    @staticmethod
    async def fetch(company_id: int):
        """Fetch an updated Company object from the API.

        .. NOTE::: Company objects are added to cache on creation.

        :param company_id: int
            The company's ID to fetch.
        :returns: Optional[:ref:`Company`]
            The company object requested.
        """
        if not company_id:
            return None

        return await internal_fetch(
            obj=Company,
            request={
                "route": "company/$company_id",
                "company_id": company_id,
                "method": "GET",
            },
        )

    @staticmethod
    async def fetch_all():
        """Fetch all companies.

        .. NOTE::: Company objects are added to cache on creation.
        """
        return await internal_fetch_all(
            obj=Company, request={"route": "company/", "method": "GET"}
        )


_companies: Dict[int, Company] = dict()
