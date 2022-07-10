from typing import List, Optional

from .. import CallBack
from IreneAPIWrapper.sections import outer
from . import AbstractModel


async def internal_fetch(obj: AbstractModel, request: dict) -> Optional[AbstractModel]:
    """Fetch an updated concrete object from the API.

    .. note::
        Concrete objects are added to cache on creation.

    :param obj: :ref:`AbstractModel`
        An abstract model.
    :param request: dict
        The request to pass into a Callback.
    :return: :ref:`AbstractModel`
        Returns an abstract model.
    """
    callback = await basic_call(request)
    if not callback.response.get("results"):
        return None
    return await obj.create(**callback.response.get("results"))


async def internal_fetch_all(obj: AbstractModel, request: dict, bulk: bool = False) -> List[AbstractModel]:
    """
    Fetch all known instances of the concrete object from the API.

    .. NOTE:: Concrete objects are added to cache on creation.

    :param obj: :ref:`AbstractModel`
        An abstract model.
    :param request: dict
        The request to pass into a Callback.
    :param bulk: bool
        Whether to generate objects in bulk (Defaults to False).
    :return: List[:ref:`AbstractModel`]
        Returns a list of abstract models.
    """
    callback = CallBack(request=request)
    await outer.client.add_and_wait(callback)

    if not callback.response.get("results"):
        return []

    if not bulk:
        return [await obj.create(**info) for info in callback.response["results"].values()]
    else:
        return await obj.create_bulk(**callback.response["results"].values())


async def internal_delete(obj: AbstractModel, request: dict) -> CallBack:
    """
    Delete the known instance of the concrete object from the API.

    .. Warning::
        This is a permanent deletion from the database. Concrete objects are removed from cache on deletion.

    :param obj: :ref:`AbstractModel`
        An abstract model.
    :param request: dict
        The request to pass into a :ref:`CallBack`.
    :returns: :ref:`CallBack`
    """
    return await basic_call(request)


async def internal_insert(request: dict) -> CallBack:
    """
    Insert an object into the database.

    :param request: dict
        The request to pass into a Callback.
    :return: :ref:`CallBack`
        Returns a :ref:`CallBack` object.
    """
    return await basic_call(request)


async def basic_call(request: dict):
    callback = CallBack(request=request)
    await outer.client.add_and_wait(callback)
    return callback
