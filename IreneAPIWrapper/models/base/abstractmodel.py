class AbstractModel:
    def __init__(self):
        """An abstract model to assist with type hints."""
        ...

    @staticmethod
    async def create(*args, **kwargs):
        ...

    @staticmethod
    async def get(unique_id: int, fetch: bool):
        ...

    @staticmethod
    async def fetch(unique_id: int):
        ...

    @staticmethod
    async def fetch_all():
        ...
