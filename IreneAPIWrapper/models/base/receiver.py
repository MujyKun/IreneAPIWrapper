from typing import List

from .. import CallBack
from IreneAPIWrapper.sections import outer
from . import AbstractModel


async def internal_fetch(obj: AbstractModel, request: dict) -> AbstractModel:
    """Fetch an updated concrete object from the API.

    # NOTE: Concrete objects are added to cache on creation.
    :param obj: (AbstractModel) An abstract model.
    :param request: (dict) The request to pass into a Callback.
    :return: (AbstractModel) Returns an abstract model.
    """
    callback = CallBack(request=request)
    await outer.client.add_and_wait(callback)
    return await obj.create(**callback.response["results"])


async def internal_fetch_all(obj: AbstractModel, request: dict) -> List[AbstractModel]:
    """
    Fetch all known instances of the concrete object from the API.

    # NOTE: Concrete objects are added to cache on creation.
    :param obj: (AbstractModel) An abstract model.
    :param request: (dict) The request to pass into a Callback.
    :return: (List[AbstractModel]) Returns a list of abstract models.
    """
    callback = CallBack(request=request)
    await outer.client.add_and_wait(callback)

    if not callback.response["results"]:
        return []

    return [await obj.create(**info) for info in callback.response["results"].values()]
