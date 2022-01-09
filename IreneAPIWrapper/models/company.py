from typing import Union, List, Optional, Dict

from IreneAPIWrapper.sections import outer
from . import CallBack, Access, AbstractModel, internal_fetch, internal_fetch_all, MediaSource, Date


class Company(AbstractModel):
    def __init__(self, company_id, name, description, date, *args, **kwargs):
        super(Company, self).__init__()
        self.id = company_id
        self.name = name
        self.description = description
        self.date: Date = date
        _companies[self.id] = self

    @staticmethod
    async def create(*args, **kwargs):
        company_id = kwargs.get("companyid")
        name = kwargs.get("name")
        description = kwargs.get("description")

        date_id = kwargs.get("dateid")
        date = await Date.get(date_id)

        return Company(*args)

    @staticmethod
    async def get(company_id: int):
        """Get a Company object.

        If the Company object does not exist in cache, it will fetch the name from the API.
        :param company_id: (int) The ID of the name to get/fetch.
        """
        existing_person = _companies.get(company_id)
        if not existing_person:
            return await Company.fetch(company_id)

    @staticmethod
    async def fetch(company_id: int):
        """Fetch an updated Company object from the API.

        # NOTE: Company objects are added to cache on creation.

        :param company_id: (int) The company's ID to fetch.
        """
        return internal_fetch(obj=Company, request={
            'route': 'company/$company_id',
            'company_id': company_id,
            'method': 'GET'}
        )

    @staticmethod
    async def fetch_all():
        """Fetch all companies.

        # NOTE: Company objects are added to cache on creation.
        """
        return internal_fetch_all(obj=Company, request={
            'route': 'company/',
            'method': 'GET'}
        )


_companies: Dict[int, Company] = dict()
